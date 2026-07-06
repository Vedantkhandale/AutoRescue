from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from config import Config
from models.users import db, User
from models.mechanic import Mechanic
from werkzeug.security import generate_password_hash, check_password_hash
from models.request import ServiceRequest


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your-secret-key-change-in-production'

db.init_app(app)


# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if user.role != role:
                return jsonify({"error": "Access denied"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==================== PUBLIC ROUTES ====================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            mobile = request.form.get("mobile", "").strip()
            password = request.form.get("password", "")
            role = request.form.get("role", "customer")

            # Validation
            if not all([name, email, mobile, password]):
                return jsonify({"error": "All fields are required"}), 400

            if len(mobile) < 10 or not mobile.isdigit():
                return jsonify({"error": "Invalid mobile number"}), 400

            if len(password) < 6:
                return jsonify({"error": "Password must be at least 6 characters"}), 400

            if User.query.filter_by(email=email).first():
                return jsonify({"error": "Email already registered"}), 400

            new_user = User(
                name=name,
                email=email,
                mobile=mobile,
                password=generate_password_hash(password),
                role=role
            )

            db.session.add(new_user)
            db.session.commit()

            return jsonify({"success": True, "message": "Registration Successful ✅"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Registration error: {str(e)}"}), 500

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            if not email or not password:
                return jsonify({"error": "Email and password are required"}), 400

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_role'] = user.role
                
                if user.role == "customer":
                    return render_template("customer_dashboard.html", user=user)
                elif user.role == "mechanic":
                    return render_template("mechanic_dashboard.html", user=user)
                elif user.role == "admin":
                    return render_template("admin_dashboard.html", user=user)

            return jsonify({"error": "Invalid Email or Password"}), 401
        except Exception as e:
            return jsonify({"error": f"Login error: {str(e)}"}), 500

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


# ==================== CUSTOMER ROUTES ====================

@app.route("/customer-dashboard")
@login_required
@role_required('customer')
def customer_dashboard():
    user = User.query.get(session['user_id'])
    requests = ServiceRequest.query.filter_by(customer_id=user.id).all()
    return render_template("customer_dashboard.html", user=user, requests=requests)


@app.route("/request-service", methods=["GET", "POST"])
@login_required
@role_required('customer')
def request_service():
    if request.method == "POST":
        try:
            vehicle_type = request.form.get("vehicle_type", "").strip()
            issue_type = request.form.get("issue_type", "").strip()
            latitude = request.form.get("latitude", "")
            longitude = request.form.get("longitude", "")

            if not all([vehicle_type, issue_type, latitude, longitude]):
                return jsonify({"error": "All fields are required"}), 400

            try:
                lat = float(latitude)
                lon = float(longitude)
            except ValueError:
                return jsonify({"error": "Invalid coordinates"}), 400

            new_request = ServiceRequest(
                customer_id=session['user_id'],
                vehicle_type=vehicle_type,
                issue_type=issue_type,
                latitude=lat,
                longitude=lon,
                status="Pending"
            )

            db.session.add(new_request)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Service request created successfully! 🚗",
                "request_id": new_request.id
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return render_template("request_service.html")


# ==================== MECHANIC ROUTES ====================

@app.route("/mechanic-dashboard")
@login_required
@role_required('mechanic')
def mechanic_dashboard():
    user = User.query.get(session['user_id'])
    mechanic = Mechanic.query.filter_by(user_id=user.id).first()
    
    # Get available requests
    available_requests = ServiceRequest.query.filter_by(status="Pending").all()
    
    return render_template("mechanic_dashboard.html", user=user, mechanic=mechanic, requests=available_requests)


@app.route("/available-requests")
@login_required
@role_required('mechanic')
def available_requests():
    requests = ServiceRequest.query.filter_by(status="Pending").all()
    return render_template("available_requests.html", requests=requests)


# ==================== SHARED ROUTES ====================

@app.route("/view-requests")
@login_required
def view_requests():
    user = User.query.get(session['user_id'])
    
    if user.role == "customer":
        requests = ServiceRequest.query.filter_by(customer_id=user.id).all()
    else:
        requests = ServiceRequest.query.all()
    
    return render_template("view_requests.html", requests=requests)


@app.route('/accept-request', methods=['POST'])
@login_required
@role_required('mechanic')
def accept_request():
    try:
        req_id = request.form.get('id') or (request.json.get('id') if request.json else None)
        
        if not req_id:
            return jsonify({"error": "Missing request ID"}), 400

        sr = ServiceRequest.query.get(int(req_id))
        if not sr:
            return jsonify({"error": "Request not found"}), 404

        sr.status = 'Accepted'
        db.session.commit()
        
        return jsonify({"success": True, "message": "Request accepted successfully! ✅"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Access denied"}), 403


# ==================== APP INITIALIZATION ====================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)

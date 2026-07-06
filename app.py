from flask import Flask, render_template, request
from config import Config
from models.users import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from models.request import ServiceRequest


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


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
                return "All fields are required", 400

            if len(mobile) < 10 or not mobile.isdigit():
                return "Invalid mobile number", 400

            if len(password) < 6:
                return "Password must be at least 6 characters", 400

            # Check if user already exists
            if User.query.filter_by(email=email).first():
                return "Email already registered", 400

            new_user = User(
                name=name,
                email=email,
                mobile=mobile,
                password=generate_password_hash(password),
                role=role
            )

            db.session.add(new_user)
            db.session.commit()

            return "Registration Successful ✅", 201
        except Exception as e:
            db.session.rollback()
            return f"Registration error: {str(e)}", 500

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            if not email or not password:
                return "Email and password are required", 400

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                if user.role == "customer":
                    return render_template("customer_dashboard.html", user=user)
                elif user.role == "mechanic":
                    return render_template("mechanic_dashboard.html", user=user)
                elif user.role == "admin":
                    return render_template("admin_dashboard.html", user=user)

            return "Invalid Email or Password", 401
        except Exception as e:
            return f"Login error: {str(e)}", 500

    return render_template("login.html")

@app.route("/request-mechanic", methods=["POST"])
def request_mechanic():
    try:
        vehicle_type = request.form.get("vehicle_type", "").strip()
        issue_type = request.form.get("issue_type", "").strip()
        latitude = request.form.get("latitude", "")
        longitude = request.form.get("longitude", "")
        customer_id = request.form.get("customer_id", 1)

        if not all([vehicle_type, issue_type, latitude, longitude]):
            return "All fields are required", 400

        try:
            lat = float(latitude)
            lon = float(longitude)
        except ValueError:
            return "Invalid latitude/longitude", 400

        new_request = ServiceRequest(
            customer_id=int(customer_id),
            vehicle_type=vehicle_type,
            issue_type=issue_type,
            latitude=lat,
            longitude=lon,
            status="Pending"
        )

        db.session.add(new_request)
        db.session.commit()

        return {"success": True, "message": "Mechanic request sent successfully 🚗", "request_id": new_request.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}, 500

@app.route("/view-requests")
def view_requests():
    try:
        requests = ServiceRequest.query.all()
        return render_template(
            "view_requests.html",
            requests=requests
        )
    except Exception as e:
        return f"Error loading requests: {str(e)}", 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)


@app.route('/accept-request', methods=['POST'])
def accept_request():
    req_id = request.form.get('id') or request.json.get('id')
    if not req_id:
        return ("Missing id", 400)

    sr = ServiceRequest.query.get(req_id)
    if not sr:
        return ("Not found", 404)

    sr.status = 'Accepted'
    db.session.commit()

    return ("Accepted", 200)
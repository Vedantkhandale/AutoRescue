from datetime import datetime
from functools import wraps
import math

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from models.mechanic import Mechanic
from models.request import ServiceRequest
from models.users import User, db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


ROLE_DASHBOARDS = {
    "customer": "customer_dashboard",
    "mechanic": "mechanic_dashboard",
    "admin": "admin_dashboard",
}


def initialize_database():
    try:
        with app.app_context():
            db.create_all()
    except Exception as error:
        app.logger.warning("Database initialization skipped: %s", error)


initialize_database()


@app.context_processor
def inject_layout_context():
    return {"current_year": datetime.utcnow().year}


def wants_json_response():
    accept_header = request.headers.get("Accept", "")
    return (
        request.path.startswith("/api/")
        or request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or "application/json" in accept_header
    )


def json_error(message, status_code=400, **payload):
    body = {"success": False, "error": message}
    body.update(payload)
    return jsonify(body), status_code


def json_success(message, status_code=200, **payload):
    body = {"success": True, "message": message}
    body.update(payload)
    return jsonify(body), status_code


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def dashboard_url_for_role(role):
    endpoint = ROLE_DASHBOARDS.get(role, "home")
    return url_for(endpoint)


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        user = get_current_user()
        if not user:
            session.clear()
            if wants_json_response():
                return json_error("Please log in to continue.", 401, redirect_url=url_for("login"))
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            user = get_current_user()
            if not user:
                session.clear()
                if wants_json_response():
                    return json_error("Please log in to continue.", 401, redirect_url=url_for("login"))
                return redirect(url_for("login"))
            if user.role != role:
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator


def parse_float(raw_value, field_name):
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.")


def parse_int(raw_value, field_name, default=0):
    if raw_value in (None, ""):
        return default
    try:
        parsed = int(raw_value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a whole number.")
    if parsed < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    return parsed


def normalize_mobile(mobile):
    return "".join(ch for ch in mobile if ch.isdigit())


def classify_request_priority(issue_type, created_at):
    issue_text = (issue_type or "").lower()
    urgent_keywords = ("accident", "brake", "engine", "flat", "smoke", "battery", "not start", "overheat")
    age_minutes = 0
    if created_at:
        age_minutes = int((datetime.utcnow() - created_at).total_seconds() // 60)

    if any(keyword in issue_text for keyword in urgent_keywords) or age_minutes <= 20:
        return "high"
    if age_minutes <= 120:
        return "medium"
    return "low"


def format_time_ago(created_at):
    if not created_at:
        return "Just now"

    delta = datetime.utcnow() - created_at
    total_minutes = int(delta.total_seconds() // 60)

    if total_minutes < 1:
        return "Just now"
    if total_minutes < 60:
        return f"{total_minutes} min ago"

    total_hours = total_minutes // 60
    if total_hours < 24:
        return f"{total_hours} hr ago"

    total_days = total_hours // 24
    suffix = "s" if total_days != 1 else ""
    return f"{total_days} day{suffix} ago"


def distance_km(origin_lat, origin_lng, target_lat, target_lng):
    if None in (origin_lat, origin_lng, target_lat, target_lng):
        return None

    radius_km = 6371
    lat1 = math.radians(origin_lat)
    lng1 = math.radians(origin_lng)
    lat2 = math.radians(target_lat)
    lng2 = math.radians(target_lng)

    delta_lat = lat2 - lat1
    delta_lng = lng2 - lng1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(radius_km * c, 1)


def serialize_request(service_request, mechanic=None, include_customer=False):
    priority = classify_request_priority(service_request.issue_type, service_request.created_at)
    customer = db.session.get(User, service_request.customer_id) if include_customer else None
    distance_label = "Location shared"

    if mechanic:
        km = distance_km(
            mechanic.latitude,
            mechanic.longitude,
            service_request.latitude,
            service_request.longitude,
        )
        if km is not None:
            distance_label = f"{km} km away"

    return {
        "id": service_request.id,
        "vehicle_type": service_request.vehicle_type,
        "issue_type": service_request.issue_type,
        "status": service_request.status,
        "priority": priority,
        "created_label": format_time_ago(service_request.created_at),
        "created_date": service_request.created_at.strftime("%d %b %Y, %I:%M %p")
        if service_request.created_at
        else "N/A",
        "latitude": round(service_request.latitude, 4),
        "longitude": round(service_request.longitude, 4),
        "distance_label": distance_label,
        "customer_name": customer.name if customer else None,
        "customer_mobile": customer.mobile if customer else None,
    }


def build_request_stats(requests):
    stats = {
        "total": len(requests),
        "pending": 0,
        "accepted": 0,
        "completed": 0,
    }
    for service_request in requests:
        status_key = service_request.status.lower()
        if status_key in stats:
            stats[status_key] += 1
    return stats


def build_home_stats():
    return {
        "mechanics": Mechanic.query.count(),
        "customers": User.query.filter_by(role="customer").count(),
        "requests": ServiceRequest.query.count(),
        "resolved": ServiceRequest.query.filter(ServiceRequest.status != "Pending").count(),
    }


@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


@app.route("/")
def home():
    stats = build_home_stats()
    return render_template("index.html", stats=stats)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            mobile = normalize_mobile(request.form.get("mobile", ""))
            password = request.form.get("password", "")
            role = request.form.get("role", "customer").strip().lower()

            if role not in {"customer", "mechanic"}:
                return json_error("Please choose a valid account type.")

            if not all([name, email, mobile, password]):
                return json_error("All required fields must be filled.")

            if len(mobile) != 10:
                return json_error("Mobile number must contain exactly 10 digits.")

            if len(password) < 6:
                return json_error("Password must be at least 6 characters long.")

            if User.query.filter_by(email=email).first():
                return json_error("This email is already registered.")

            new_user = User(
                name=name,
                email=email,
                mobile=mobile,
                password=generate_password_hash(password),
                role=role,
            )
            db.session.add(new_user)
            db.session.flush()

            if role == "mechanic":
                shop_name = request.form.get("shop_name", "").strip()
                experience = parse_int(request.form.get("experience"), "Experience", default=0)
                latitude = parse_float(request.form.get("latitude"), "Latitude")
                longitude = parse_float(request.form.get("longitude"), "Longitude")

                if not shop_name:
                    raise ValueError("Shop name is required for mechanic accounts.")

                db.session.add(
                    Mechanic(
                        user_id=new_user.id,
                        shop_name=shop_name,
                        experience=experience,
                        latitude=latitude,
                        longitude=longitude,
                        availability="Available",
                        rating=4.8,
                    )
                )

            db.session.commit()
            return json_success(
                "Account created successfully. You can log in now.",
                201,
                redirect_url=url_for("login"),
            )
        except ValueError as error:
            db.session.rollback()
            return json_error(str(error))
        except Exception as error:
            db.session.rollback()
            return json_error(f"Registration failed: {error}", 500)

    selected_role = request.args.get("role", "customer").strip().lower()
    if selected_role not in {"customer", "mechanic"}:
        selected_role = "customer"
    return render_template("register.html", selected_role=selected_role)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            if not email or not password:
                return json_error("Email and password are required.")

            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                return json_error("Invalid email or password.", 401)

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role

            return json_success(
                f"Welcome back, {user.name}.",
                redirect_url=dashboard_url_for_role(user.role),
            )
        except Exception as error:
            return json_error(f"Login failed: {error}", 500)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/customer-dashboard")
@login_required
@role_required("customer")
def customer_dashboard():
    user = get_current_user()
    requests = (
        ServiceRequest.query.filter_by(customer_id=user.id)
        .order_by(ServiceRequest.created_at.desc())
        .all()
    )
    stats = build_request_stats(requests)
    return render_template("customer_dashboard.html", user=user, requests=requests, stats=stats)


@app.route("/request-service", methods=["GET", "POST"])
@login_required
@role_required("customer")
def request_service():
    if request.method == "POST":
        try:
            vehicle_type = request.form.get("vehicle_type", "").strip()
            issue_type = request.form.get("issue_type", "").strip()
            latitude = parse_float(request.form.get("latitude"), "Latitude")
            longitude = parse_float(request.form.get("longitude"), "Longitude")

            if not vehicle_type or not issue_type:
                return json_error("Vehicle type and issue description are required.")

            if len(issue_type) < 10:
                return json_error("Please add a clearer issue description.")

            new_request = ServiceRequest(
                customer_id=session["user_id"],
                vehicle_type=vehicle_type,
                issue_type=issue_type,
                latitude=latitude,
                longitude=longitude,
                status="Pending",
            )

            db.session.add(new_request)
            db.session.commit()

            return json_success(
                "Rescue request created. Nearby mechanics can see it now.",
                201,
                redirect_url=url_for("view_requests"),
                request_id=new_request.id,
            )
        except ValueError as error:
            db.session.rollback()
            return json_error(str(error))
        except Exception as error:
            db.session.rollback()
            return json_error(f"Could not create request: {error}", 500)

    return render_template("request_service.html", user=get_current_user())


@app.route("/mechanic-dashboard")
@login_required
@role_required("mechanic")
def mechanic_dashboard():
    user = get_current_user()
    mechanic = Mechanic.query.filter_by(user_id=user.id).first()
    pending_requests = (
        ServiceRequest.query.filter_by(status="Pending")
        .order_by(ServiceRequest.created_at.desc())
        .all()
    )
    network_stats = build_request_stats(ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all())
    enriched_requests = [serialize_request(item, mechanic, include_customer=True) for item in pending_requests[:6]]
    return render_template(
        "mechanic_dashboard.html",
        user=user,
        mechanic=mechanic,
        requests=enriched_requests,
        stats=network_stats,
    )


@app.route("/available-requests")
@login_required
@role_required("mechanic")
def available_requests():
    user = get_current_user()
    mechanic = Mechanic.query.filter_by(user_id=user.id).first()
    pending_requests = (
        ServiceRequest.query.filter_by(status="Pending")
        .order_by(ServiceRequest.created_at.desc())
        .all()
    )
    request_cards = [serialize_request(item, mechanic, include_customer=True) for item in pending_requests]
    return render_template("available_requests.html", requests=request_cards, mechanic=mechanic)


@app.route("/view-requests")
@login_required
def view_requests():
    user = get_current_user()
    if user.role == "customer":
        query = ServiceRequest.query.filter_by(customer_id=user.id)
    else:
        query = ServiceRequest.query

    requests = query.order_by(ServiceRequest.created_at.desc()).all()
    return render_template(
        "view_requests.html",
        user=user,
        requests=requests,
        can_accept=user.role == "mechanic",
    )


@app.route("/admin-dashboard")
@login_required
@role_required("admin")
def admin_dashboard():
    user = get_current_user()
    recent_users = User.query.order_by(User.created_at.desc()).limit(8).all()
    recent_requests = (
        ServiceRequest.query.order_by(ServiceRequest.created_at.desc())
        .limit(8)
        .all()
    )
    stats = {
        "users": User.query.count(),
        "mechanics": Mechanic.query.count(),
        "pending": ServiceRequest.query.filter_by(status="Pending").count(),
        "completed": ServiceRequest.query.filter_by(status="Completed").count(),
    }
    return render_template(
        "admin_dashboard.html",
        user=user,
        users=recent_users,
        requests=recent_requests,
        stats=stats,
    )


@app.route("/accept-request", methods=["POST"])
@login_required
@role_required("mechanic")
def accept_request():
    try:
        payload = request.get_json(silent=True) or request.form
        raw_request_id = payload.get("id") if payload else None

        if not raw_request_id:
            return json_error("Request ID is required.")

        service_request = db.session.get(ServiceRequest, int(raw_request_id))
        if not service_request:
            return json_error("Request not found.", 404)

        if service_request.status != "Pending":
            return json_error("This request has already been handled.", 409)

        service_request.status = "Accepted"
        db.session.commit()
        return json_success("Request accepted successfully.")
    except ValueError:
        db.session.rollback()
        return json_error("Request ID must be numeric.")
    except Exception as error:
        db.session.rollback()
        return json_error(f"Could not accept request: {error}", 500)


@app.errorhandler(403)
def forbidden(_error):
    if wants_json_response():
        return json_error("Access denied.", 403)
    return render_template("error.html", status_code=403, message="Access denied."), 403


@app.errorhandler(404)
def not_found(_error):
    if wants_json_response():
        return json_error("Resource not found.", 404)
    return render_template("error.html", status_code=404, message="Page not found."), 404


@app.errorhandler(500)
def internal_error(_error):
    db.session.rollback()
    if wants_json_response():
        return json_error("Internal server error.", 500)
    return render_template("error.html", status_code=500, message="Something broke on our side."), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

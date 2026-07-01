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

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        new_user = User(
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return "Registration Successful ✅"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            if user.role == "customer":
                return render_template("customer_dashboard.html")

            elif user.role == "mechanic":
                return render_template("mechanic_dashboard.html")

            elif user.role == "admin":
                return render_template("admin_dashboard.html")

        return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/request-mechanic", methods=["POST"])
def request_mechanic():

    vehicle_type = request.form["vehicle_type"]
    issue_type = request.form["issue_type"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    new_request = ServiceRequest(
        customer_id=1,
        vehicle_type=vehicle_type,
        issue_type=issue_type,
        latitude=latitude,
        longitude=longitude,
        status="Pending"
    )

    db.session.add(new_request)
    db.session.commit()

    return "Mechanic Request Sent Successfully 🚗"

@app.route("/view-requests")
def view_requests():

    requests = ServiceRequest.query.all()

    return render_template(
        "view_requests.html",
        requests=requests
    )


if __name__ == "__main__":
    app.run(debug=True)


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
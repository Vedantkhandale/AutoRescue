from flask import Flask, render_template, request
from config import Config
from models.users import db, User
from werkzeug.security import generate_password_hash, check_password_hash

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
                return "Mechanic Dashboard"

            elif user.role == "admin":
                return "Admin Dashboard"

        return "Invalid Email or Password"

    return render_template("login.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
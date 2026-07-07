from sqlalchemy import text
from werkzeug.security import generate_password_hash

from app import app, db
from models.mechanic import Mechanic
from models.request import ServiceRequest
from models.users import User


def seed_test_data():
    with app.app_context():
        db.create_all()

        if User.query.first():
            print("Database already has data. Skipping seed.")
            return

        customer = User(
            name="John Doe",
            email="customer@example.com",
            mobile="9876543210",
            password=generate_password_hash("password123"),
            role="customer",
        )
        mechanic_user = User(
            name="Raj Kumar",
            email="mechanic@example.com",
            mobile="9123456789",
            password=generate_password_hash("password123"),
            role="mechanic",
        )
        admin = User(
            name="Admin User",
            email="admin@example.com",
            mobile="9000000000",
            password=generate_password_hash("admin123"),
            role="admin",
        )

        db.session.add_all([customer, mechanic_user, admin])
        db.session.flush()

        mechanic = Mechanic(
            user_id=mechanic_user.id,
            shop_name="Raj Auto Repair",
            experience=6,
            latitude=28.6139,
            longitude=77.2090,
            availability="Available",
            rating=4.8,
        )

        requests = [
            ServiceRequest(
                customer_id=customer.id,
                vehicle_type="Bike",
                issue_type="Bike engine is not starting and there is smoke near the exhaust.",
                latitude=28.6200,
                longitude=77.2150,
                status="Pending",
            ),
            ServiceRequest(
                customer_id=customer.id,
                vehicle_type="Car",
                issue_type="Front left tyre burst near office parking, need urgent replacement.",
                latitude=28.6080,
                longitude=77.2015,
                status="Accepted",
            ),
        ]

        db.session.add(mechanic)
        db.session.add_all(requests)
        db.session.commit()

        print("Seed complete.")
        print("Customer: customer@example.com / password123")
        print("Mechanic: mechanic@example.com / password123")
        print("Admin: admin@example.com / admin123")


def verify_database():
    with app.app_context():
        db.session.execute(text("SELECT 1"))
        print(f"Users: {User.query.count()}")
        print(f"Mechanics: {Mechanic.query.count()}")
        print(f"Requests: {ServiceRequest.query.count()}")


if __name__ == "__main__":
    seed_test_data()
    verify_database()

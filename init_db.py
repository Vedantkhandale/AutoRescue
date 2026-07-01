"""Initialize local database and seed basic data.

Run: python init_db.py
"""
from app import app
from models.users import db, User
from models.request import ServiceRequest
from models.mechanic import Mechanic
from werkzeug.security import generate_password_hash


def seed():
    with app.app_context():
        db.create_all()

        # Add a customer user
        if not User.query.filter_by(email='customer@example.com').first():
            c = User(
                name='Test Customer',
                email='customer@example.com',
                mobile='9999999999',
                password=generate_password_hash('password'),
                role='customer'
            )
            db.session.add(c)

        # Add a mechanic user
        if not User.query.filter_by(email='mechanic@example.com').first():
            muser = User(
                name='Test Mechanic',
                email='mechanic@example.com',
                mobile='8888888888',
                password=generate_password_hash('password'),
                role='mechanic'
            )
            db.session.add(muser)
            db.session.flush()

            mech = Mechanic(
                user_id=muser.id,
                shop_name='QuickFix Garage',
                experience=5,
                latitude='28.7041',
                longitude='77.1025',
                availability='Available'
            )
            db.session.add(mech)

        # Add a sample service request
        if not ServiceRequest.query.first():
            # Use the first customer
            cust = User.query.filter_by(role='customer').first()
            sr = ServiceRequest(
                customer_id=cust.id if cust else 1,
                vehicle_type='Car',
                issue_type='Flat tyre',
                latitude='28.7041',
                longitude='77.1025',
                status='Pending'
            )
            db.session.add(sr)

        db.session.commit()


if __name__ == '__main__':
    seed()
    print('Database initialized and seeded: autorescue.db')

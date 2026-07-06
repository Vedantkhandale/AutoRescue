"""
Initialize AutoRescue database and seed with test data.

REQUIREMENTS:
1. XAMPP must be running with MySQL service active
2. Database credentials must match config.py

To setup:
1. Start XAMPP (MySQL service)
2. Run: python init_db.py

This will:
- Create the database 'autorescue_v2'
- Create all tables
- Seed with test users (customer, mechanic, admin)
"""

import os
import sys
from app import app, db
from models.users import User
from models.request import ServiceRequest
from models.mechanic import Mechanic
from werkzeug.security import generate_password_hash


def create_database():
    """Create database and all tables"""
    try:
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False
    return True


def seed_test_data():
    """Seed database with test data"""
    try:
        with app.app_context():
            print("\n📝 Seeding test data...")
            
            # Check if data already exists
            if User.query.first():
                print("⚠️  Database already contains data. Skipping seed.")
                return True
            
            # Test Customer
            customer = User(
                name='John Doe',
                email='customer@example.com',
                mobile='9876543210',
                password=generate_password_hash('password123'),
                role='customer'
            )
            db.session.add(customer)
            
            # Test Mechanic User
            mechanic_user = User(
                name='Raj Kumar',
                email='mechanic@example.com',
                mobile='9123456789',
                password=generate_password_hash('password123'),
                role='mechanic'
            )
            db.session.add(mechanic_user)
            
            # Test Admin
            admin = User(
                name='Admin User',
                email='admin@example.com',
                mobile='9000000000',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            
            db.session.commit()
            
            # Add mechanic details
            mechanic = Mechanic(
                user_id=mechanic_user.id,
                shop_name='Raj Auto Repair Shop',
                experience=5,
                latitude=28.6139,
                longitude=77.2090,
                availability='Available',
                rating=4.5
            )
            db.session.add(mechanic)
            
            # Add test service request
            service_req = ServiceRequest(
                customer_id=customer.id,
                vehicle_type='Bike',
                issue_type='Engine Problem',
                latitude=28.6200,
                longitude=77.2150,
                status='Pending'
            )
            db.session.add(service_req)
            
            db.session.commit()
            
            print("✅ Test data seeded successfully!")
            print(f"\nTest Accounts:")
            print(f"  Customer: customer@example.com / password123")
            print(f"  Mechanic: mechanic@example.com / password123")
            print(f"  Admin: admin@example.com / admin123")
            
    except Exception as e:
        print(f"❌ Error seeding data: {str(e)}")
        db.session.rollback()
        return False
    
    return True


def verify_database():
    """Verify database connection and tables"""
    try:
        with app.app_context():
            from sqlalchemy import text
            # Test connection
            db.session.execute(text('SELECT 1'))
            
            # Count records
            user_count = User.query.count()
            request_count = ServiceRequest.query.count()
            
            print(f"\n📊 Database Status:")
            print(f"  Users: {user_count}")
            print(f"  Service Requests: {request_count}")
            
            return True
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚗 AutoRescue Database Setup")
    print("=" * 50)
    
    if not create_database():
        sys.exit(1)
    
    if not seed_test_data():
        sys.exit(1)
    
    if not verify_database():
        print("\n⚠️  Could not verify database, but tables may have been created.")
        print("Ensure XAMPP MySQL is running and credentials in config.py are correct.")
    
    print("\n" + "=" * 50)
    print("✅ Database setup complete!")
    print("\nNext steps:")
    print("1. Run: python app.py")
    print("2. Open: http://127.0.0.1:5000")
    print("3. Login with test credentials above")

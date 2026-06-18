from models.users import db

class ServiceRequest(db.Model):

    __tablename__ = "service_requests"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer)

    vehicle_type = db.Column(db.String(50))

    issue_type = db.Column(db.String(255))

    latitude = db.Column(db.String(50))

    longitude = db.Column(db.String(50))

    status = db.Column(db.String(20))
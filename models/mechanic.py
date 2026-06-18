from models.users import db

class Mechanic(db.Model):

    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    shop_name = db.Column(db.String(100))

    experience = db.Column(db.Integer)

    latitude = db.Column(db.String(50))

    longitude = db.Column(db.String(50))

    availability = db.Column(db.String(20))
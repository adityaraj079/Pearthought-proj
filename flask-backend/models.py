from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    notification_preference = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')

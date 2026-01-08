from app import db

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.Enum('admin', 'receptionist', 'manager', 'staff'), default='staff')
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))
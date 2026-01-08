# app/models/operation.py
from app import db
from datetime import datetime

class Guest(db.Model):
    __tablename__ = 'Guests'
    guest_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50))
    address = db.Column(db.String(105))
    nationality = db.Column(db.String(40))
    # Relationship to GuestPhones (One-to-Many)
    phones = db.relationship('GuestPhone', backref='guest', lazy=True)

class GuestPhone(db.Model):
    __tablename__ = 'GuestPhones'
    phone_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('Guests.guest_id'))
    phone_number = db.Column(db.String(20))
    phone_type = db.Column(db.String(20))

class Booking(db.Model):
    __tablename__ = 'Bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('Guests.guest_id'))
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.room_id'))
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    total_amount = db.Column(db.Numeric(10, 2))
    booking_status = db.Column(db.Enum('active', 'completed', 'cancelled'), default='active')
    
    # Relationships
    payments = db.relationship('Payment', backref='booking', lazy=True)
    feedback = db.relationship('Feedback', backref='booking', uselist=False)

class Payment(db.Model):
    __tablename__ = 'Payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('Bookings.booking_id'))
    payment_method = db.Column(db.Enum('cash', 'card', 'online'), default='cash')
    amount_paid = db.Column(db.Numeric(10, 2))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    feedback_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('Guests.guest_id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('Bookings.booking_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

class ServiceOrder(db.Model):
    __tablename__ = 'ServiceOrders'
    order_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('Bookings.booking_id'))
    service_id = db.Column(db.Integer, db.ForeignKey('Services.service_id'))
    quantity = db.Column(db.Integer, default=1)
    total_order_cost = db.Column(db.Numeric(10, 2))

class AuditLog(db.Model):
    __tablename__ = 'AuditLog'
    log_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50))
    action_type = db.Column(db.String(10))
    details = db.Column(db.Text)
    action_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
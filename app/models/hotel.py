from app import db

class RoomType(db.Model):
    __tablename__ = 'RoomTypes'
    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    base_price = db.Column(db.Numeric(10, 2))
    max_persons = db.Column(db.Integer)

class Room(db.Model):
    __tablename__ = 'Rooms'
    room_id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey('RoomTypes.type_id'))
    status = db.Column(db.Enum('available', 'booked', 'maintenance'), default='available')

class Service(db.Model):
    __tablename__ = 'Services'
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
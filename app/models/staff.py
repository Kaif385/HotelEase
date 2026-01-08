from app import db

class Employee(db.Model):
    __tablename__ = 'Employees'
    emp_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))
    shift_time = db.Column(db.String(50))
    salary = db.Column(db.Numeric(10, 2))
    hire_date = db.Column(db.Date)

class Maintenance(db.Model):
    __tablename__ = 'Maintenance'
    task_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.room_id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('Employees.emp_id'))
    task_desc = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'completed'), default='pending')
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bus(db.Model):
    __tablename__ = 'bus'
    
    Bus_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Bus_Number = db.Column(db.String(50), nullable=False)
    Bus_Type = db.Column(db.String(50), nullable=False)
    Capacity = db.Column(db.Integer, nullable=False)
    Operator_Name = db.Column(db.String(100))
    Route_ID = db.Column(db.Integer, db.ForeignKey('route.Route_ID'))

    # Relationships
    route = db.relationship('Route', back_populates='buses')
    schedules = db.relationship('Schedule', back_populates='bus')
    drivers = db.relationship('Driver', back_populates='bus')


class Route(db.Model):
    __tablename__ = 'route'

    Route_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Source = db.Column(db.String(100), nullable=False)
    Destination = db.Column(db.String(100), nullable=False)
    Distance = db.Column(db.Numeric(5, 2))
    Estimated_Travel_Time = db.Column(db.Time)

    # Relationships
    buses = db.relationship('Bus', back_populates='route')
    schedules = db.relationship('Schedule', back_populates='route')


class Schedule(db.Model):
    __tablename__ = 'schedule'

    Schedule_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Bus_ID = db.Column(db.Integer, db.ForeignKey('bus.Bus_ID'))
    Route_ID = db.Column(db.Integer, db.ForeignKey('route.Route_ID'))
    Departure_Time = db.Column(db.DateTime, nullable=False)
    Arrival_Time = db.Column(db.DateTime, nullable=False)

    # Relationships
    bus = db.relationship('Bus', back_populates='schedules')
    route = db.relationship('Route', back_populates='schedules')
    reservations = db.relationship('Reservation', back_populates='schedule')


class Passenger(db.Model):
    __tablename__ = 'passenger'

    Passenger_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    Age = db.Column(db.Integer)
    Contact_Number = db.Column(db.String(15))
    Email = db.Column(db.String(100))

    # Relationship
    reservations = db.relationship('Reservation', back_populates='passenger')


class Reservation(db.Model):
    __tablename__ = 'reservation'

    Reservation_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Passenger_ID = db.Column(db.Integer, db.ForeignKey('passenger.Passenger_ID'))
    Schedule_ID = db.Column(db.Integer, db.ForeignKey('schedule.Schedule_ID'))
    Seat_Number = db.Column(db.Integer, nullable=False)
    Reservation_Date = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.Enum('Confirmed', 'Cancelled'), nullable=False)

    # Relationships
    passenger = db.relationship('Passenger', back_populates='reservations')
    schedule = db.relationship('Schedule', back_populates='reservations')
    payment = db.relationship('Payment', back_populates='reservation', uselist=False)  # Ensure this line is correct


class Payment(db.Model):
    __tablename__ = 'payment'

    Payment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Reservation_ID = db.Column(db.Integer, db.ForeignKey('reservation.Reservation_ID'))
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    Payment_Date = db.Column(db.DateTime, nullable=False)
    Payment_Method = db.Column(db.Enum('Credit Card', 'Debit Card', 'Net Banking'), nullable=False)

    # Relationship
    reservation = db.relationship('Reservation', back_populates='payment')  # Ensure this line is correct


class Driver(db.Model):
    __tablename__ = 'driver'

    Driver_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    License_Number = db.Column(db.String(50), nullable=False)
    Contact_Number = db.Column(db.String(15))
    Bus_ID = db.Column(db.Integer, db.ForeignKey('bus.Bus_ID'))

    # Relationship
    bus = db.relationship('Bus', back_populates='drivers')


class User(db.Model):
    __tablename__ = 'user'

    User_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    Email = db.Column(db.String(100), unique=True)
    IsAdmin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<User {self.Username}>'

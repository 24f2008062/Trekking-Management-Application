from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)
user_roles = db.Table(
    'user_roles',

    db.Column(
        'user_id',
        db.ForeignKey('user.id'),
        primary_key=True
    ),

    db.Column(
        'role_id',
        db.ForeignKey('role.id'),
        primary_key = True
    )
)
user_booking = db.Table(
    'user_booking',

    db.Column(
        'user_id',
        db.ForeignKey('user.id'),
        primary_key=True
    ),

    db.Column(
        'booking_id',
        db.ForeignKey('booking.id')
    )
)
class User(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    username = db.Column(
        db.String(200), 
        nullable=False, 
        unique=True
    )

    email = db.Column(
        db.String(200), 
        nullable=False, 
        unique=True
    )

    password = db.Column(
        db.String(300), 
        nullable=False
    )

    role = db.relationship(
        "Role",
        secondary = user_roles,
        back_populates='user')

class Role(db.Model):

    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    rolename = db.Column(
        db.String(200),
        nullable=False,
        unique=True
    )
    user = db.relationship(
        User,
        secondary=user_roles,
        back_populates = 'role'
    )

class trek(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    difficulty = db.Column(
        db.String(200),
        nullable=False,
    )
    duration = db.Column(
        db.String(200),
    )
    available_slots = db.Column(
        db.Integer
    )

    # Assingned Staff
    
    status = db.Column(
        db.String(200)
    )

class Booking(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Relationship(
        'Booking',
        secondary=user_booking,
        back_populates='user_id'
    )
    trek_id = db.Column(
        db.Integer,
        db.ForeignKey('trek.id')
    )
    booking_staus = db.Column(
        db.String(200),
        nullable=False
    )
    booking_date = db.Column(
        db.Date(),
        nullable=False
    )
    payment_status = db.Column(
        db.String(200),
    )

class staff_profile(db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        unique=True,
        nullable=False
    )
    phone = db.Column(
        db.Integer,
        unique=True
    )
    Address = db.Column(
        db.String(200),
        nullable=False
    )
    


with app.app_context():
    db.create_all()
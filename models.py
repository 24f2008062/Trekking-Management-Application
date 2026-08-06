from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
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

    name = db.Column(
        db.String(200),
        nullable=False
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

    profile = db.relationship(
        "staff_profile",
        uselist=False,
        backref='user'
    )


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
    name = db.Column(
        db.String(200),
        nullable=False
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
    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True
    )
    assigned_staff = db.relationship(
        'User',
        foreign_keys=[assigned_staff_id],
        backref='assigned_treks'
    )

    status = db.Column(
        db.String(200)
    )

    bookings = db.relationship(
        'Booking',
        backref='trek'
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
        db.Integer
    )
    Address = db.Column(
        db.String(200),
        nullable=False
    )

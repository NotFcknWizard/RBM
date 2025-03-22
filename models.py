from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default="user", nullable=False)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="pending")

    user = db.relationship("User", backref="registrations", cascade="all, delete")


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainer = db.Column(db.String(300) ,nullable = False)
    place = db.Column(db.Text,nullable = False)
    price = db.Column(db.Integer , nullable = False)
    loggedby = db.Column(db.Integer , nullable = False)
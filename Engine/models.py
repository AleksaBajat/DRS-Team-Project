from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):        
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    phoneNumber = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    accounts = db.relationship('Account')


class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    balance = db.Column(db.Integer, default=0)
    currency = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Transaction(db.Model):
    id = db.Column(db.String, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recipient = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String, default="Processing")
# Agenix/models.py
from flask_login import UserMixin
from database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(1000))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), default='New Chat')
    thread_id = db.Column(db.String(36), unique=True, nullable=False)
    user = db.relationship('User', backref=db.backref('chats', lazy=True))
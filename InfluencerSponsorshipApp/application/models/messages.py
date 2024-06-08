from flask_login import UserMixin
from application.database import db
from datetime import datetime


class Message(db.Model,UserMixin):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20),nullable=False)
    sent_by = db.Column(db.String(20),nullable=False)
    sent_to = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    read  = db.Column(db.Boolean,nullable=False)
    sent_date = db.Column(db.Date,nullable=False)

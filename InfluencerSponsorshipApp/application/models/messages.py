from flask_login import UserMixin
from application.database import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20),nullable=False)
    sent_by = db.Column(db.String(20),nullable=False)
    sent_to = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    read  = db.Column(db.Boolean,nullable=False)
    sent_date = db.Column(db.DateTime,nullable=False)
    type = db.Column(db.String(10),nullable=False)
    message_id = db.Column(db.Integer)

    def __init__(self,title,description,sent_by,sent_to,sent_date,type,message_id):
        self.title = title
        self.sent_by = sent_by
        self.sent_to = sent_to
        self.description = description
        self.sent_date = sent_date
        self.read = False
        self.type=type
        self.message_id = message_id
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



class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key = True)
    complain = db.Column(db.String(100),nullable=False)
    reported_by = db.Column(db.String(20),nullable=False)
    report_against = db.Column(db.String(20),nullable=False)
    sent_date = db.Column(db.DateTime,nullable=False)
    report_type = db.Column(db.String(20),nullable=False)

    def __init__(self,complain,reported_by,report_against,sent_date,report_type):
        self.reported_by = reported_by
        self.report_against = report_against
        self.complain = complain
        self.sent_date = sent_date
        self.report_type = report_type

class Negotiate(db.Model):
    __tablename__ = 'negotiate'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20),nullable=False)
    sent_by = db.Column(db.String(20),nullable=False)
    sent_to = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    read  = db.Column(db.Boolean,nullable=False)
    sent_date = db.Column(db.DateTime,nullable=False)
    type = db.Column(db.String(10),nullable=False)
    message_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)


    def __init__(self,title,description,sent_by,sent_to,sent_date,type,message_id,amount):
        self.title = title
        self.sent_by = sent_by
        self.sent_to = sent_to
        self.description = description
        self.sent_date = sent_date
        self.read = False
        self.type=type
        self.message_id = message_id
        self.amount = amount


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20),nullable=False)
    sent_by = db.Column(db.String(20),nullable=False)
    sent_to = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    read  = db.Column(db.Boolean,nullable=False)
    sent_date = db.Column(db.DateTime,nullable=False)
    type = db.Column(db.String(10),nullable=False)
    message_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)


    def __init__(self,title,description,sent_by,sent_to,sent_date,type,message_id,amount):
        self.title = title
        self.sent_by = sent_by
        self.sent_to = sent_to
        self.description = description
        self.sent_date = sent_date
        self.read = False
        self.type=type
        self.message_id = message_id
        self.amount = amount
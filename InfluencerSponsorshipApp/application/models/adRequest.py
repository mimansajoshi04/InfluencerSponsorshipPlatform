
from application.database import db
from datetime import datetime


class AdRequest(db.Model):
    __tablename__ = 'ad'

    id = db.Column(db.Integer, primary_key = True)
    campaign_id = db.Column(db.Integer)
    influencer = db.Column(db.String(100))
    sponsor = db.Column(db.String(100))
    name = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    status = db.Column(db.String(100),nullable=False)
    deleted  = db.Column(db.Boolean,nullable=False)
    payment_amount = db.Column(db.Integer)

    def __init__(self,name,description,campaign_id,influencer,sponsor,status,payment_amount):
        self.name = name
        self.campaign_id = campaign_id
        self.influencer = influencer
        self.sponsor = sponsor
        self.status = status
        self.description = description
        self.deleted = False
        self.payment_amount = payment_amount
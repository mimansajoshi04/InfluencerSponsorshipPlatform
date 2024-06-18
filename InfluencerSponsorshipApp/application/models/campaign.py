
from application.database import db
from datetime import datetime


class Campaign(db.Model):
    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    start_date = db.Column(db.DateTime,nullable=False,default = datetime.now())
    end_date = db.Column(db.DateTime,nullable=False,default = datetime.now())
    niche = db.Column(db.String(1000),nullable=False)
    category = db.Column(db.String(100),nullable=False)
    industry = db.Column(db.String(100),nullable=False)
    isflagged  = db.Column(db.Boolean,nullable=False)
    goals = db.Column(db.String(100),nullable=False)
    started_by = db.Column(db.String(20),nullable=False)
    visibility = db.Column(db.String(10),nullable=False)
    reports = db.Column(db.Integer)
    budget = db.Column(db.Integer)

    def __init__(self,name,description,start_date,end_date,started_by,visibility,niche,category,goals,budget,industry):
        self.name = name
        self.started_by = started_by
        self.start_date= start_date
        self.end_date= end_date
        self.description = description
        self.isflagged = False
        self.visibility=visibility
        self.reports = 0
        self.niche = niche
        self.category = category
        self.goals = goals
        self.budget = budget
        self.industry = industry
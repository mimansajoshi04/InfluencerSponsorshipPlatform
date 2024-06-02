from flask_login import UserMixin
from application.database import db
from datetime import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model,UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80),nullable=False,unique=True)
    userType = db.Column(db.String(20),nullable=False,unique=True)


    def __init__(self,username,userType):
        self.username = username
        self.userType = userType
    

class Admin(db.Model,UserMixin):
    __table__name = 'admin'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(80),db.ForeignKey('user.username'),nullable=False,unique=True)
    email = db.Column(db.String(80),nullable=False,unique=True)
    userType = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)

    def __init__(self,name,username,email,password,userType):

        self.name = name
        self.username = username
        self.email = email
        self.userType = userType
        self.password = generate_password_hash(password)

    
    def checkPassowrd(self,password):
        return check_password_hash(self.password,password)


class Influencer(db.Model,UserMixin):
    __tablename__ = 'influencer'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(80),db.ForeignKey('user.username'),nullable=False,unique=True)
    email = db.Column(db.String(80),nullable=False,unique=True)
    category = db.Column(db.String(80),nullable=False,unique=True)
    niche = db.Column(db.String(80),nullable=False,unique=True)
    profilePicture = db.Column(db.String(100),nullable=False)
    userType = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)

    def __init__(self,name,username,email,password,userType,category,niche):

        self.name = name
        self.username = username
        self.email = email
        self.userType = userType
        self.category = category
        self.niche = niche
        self.profilePicture = ""
        self.password = generate_password_hash(password)

    
    def checkPassowrd(self,password):
        return check_password_hash(self.password,password)


class Sponsor(db.Model,UserMixin):
    __tablename__ = 'sponsor'

    id = db.Column(db.Integer, primary_key = True)
    companyName = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(80),db.ForeignKey('user.username'),nullable=False,unique=True)
    email = db.Column(db.String(80),nullable=False,unique=True)
    budget = db.Column(db.Integer,nullable=False)
    profilePicture = db.Column(db.String(100),nullable=False)
    userType = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)

    def __init__(self,name,username,email,password,userType,budget):

        self.companyName = name
        self.username = username
        self.email = email
        self.userType = userType
        self.budget = budget
        self.profilePicture =""
        self.password = generate_password_hash(password)

    
    def checkPassowrd(self,password):
        return check_password_hash(self.password,password)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine




app = Flask(__name__,static_folder="../static",template_folder="../templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this is my secret key no one can access'
app.config['SQLALCHEMY_POOL_SIZE'] = 20

engine = create_engine('sqlite:///testdb.db')

db = SQLAlchemy(app)    
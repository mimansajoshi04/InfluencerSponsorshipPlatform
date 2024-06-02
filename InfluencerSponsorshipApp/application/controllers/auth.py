
from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user

from application.models.user import User


@app.route('/')
def index():
    return render_template("/auth/login.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        
        username = request.form["username"]
        password = request.form["password"]

        connection = db.engine.connect()
        query= text("SELECT username FROM users WHERE username = :username")
        result = connection.execute(query,{'username':username})

        if result.fetchone() is None:
            flash("Username does not exist. Check again or click on register to register.")
            return render_template('auth/login.html')
        

        query=text("SELECT password FROM users WHERE username= :username")
        result = connection.execute(query,{'username':username})

        row=result.fetchone()
        
        if check_password_hash(row[0],password):
            session['username'] = username
            query= text("SELECT * FROM users WHERE username = :username")
            result = connection.execute(query,{'username':username})
            user = result.fetchall()
            userSession = User.query.filter_by(username=username).first()

            if user[0][7] != 1:
                login_user(userSession)
                return redirect(url_for('dashboard'))
            else:
                login_user(userSession)
                return redirect(url_for('adminDashboard'))
        
        else:
            flash("Password is incorrect. Try again.")
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        return 
    return render_template('/auth/register.html')


from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user

from application.models.user import *

@app.route("/dashboard")
def dashboard():
    
    connection = db.engine.connect()
    query= text("SELECT userType FROM user WHERE username = :username")
    result = connection.execute(query,{'username':session["username"]})

    row = result.fetchone()
    if row[0] == "admin":
        return redirect(url_for("adminDashboard"))
    elif row[0] == "influencer":
        return redirect(url_for("influencerDashboard"))
    else:
        return redirect(url_for("sponsorDashboard"))



@app.route('/')
def index():
    if 'username' in session:
        flash(f"Logged in as {session['username']}")
        return redirect(url_for("dashboard"))
    
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        
        username = request.form["username"]
        password = request.form["password"]

        connection = db.engine.connect()
        query= text("SELECT username FROM user WHERE username = :username")
        result = connection.execute(query,{'username':username})


        if result.fetchone() is None:
            flash("Username does not exist. Check again or click on register to register.")
            return render_template('auth/login.html')
        

        query=text("SELECT password FROM user WHERE username= :username")
        result = connection.execute(query,{'username':username})

        row=result.fetchone()
        
        if check_password_hash(row[0],password):
            session['username'] = username
            query= text("SELECT * FROM user WHERE username = :username")
            result = connection.execute(query,{'username':username})
            user = result.fetchall()
            userSession = User.query.filter_by(username=username).first()

            with db.engine.begin() as connection:
                query = text("UPDATE user SET isActive = 1 WHERE username = :username")
                details = {"username" : username}
                connection.execute(query,details)

            if user[0][2] == "admin":
                login_user(userSession)
                return redirect(url_for('adminDashboard'))
            
            elif user[0][2] == "influencer":
                login_user(userSession)
                return redirect(url_for('influencerDashboard'))
            
            else:
                login_user(userSession)
                return redirect(url_for('sponsorDashboard'))
        
        else:
            flash("Password is incorrect. Try again.")
            return render_template('auth/login.html')

    return render_template('auth/login.html')


@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":

        

        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        email = request.form["email"]


        session["username"] = username
        session["name"] = name
        session["email"] = email
        session["password"] = password

        connection = db.engine.connect()
        query = text("SELECT username FROM user WHERE username = :username")
        result = connection.execute(query,{"username": username})

        if result.fetchone() is not None:
            flash("Username already exists.")
            return render_template("/auth/register.html")
        
        connection = db.engine.connect()
        query = text("SELECT email FROM user WHERE email = :email")
        result = connection.execute(query,{"email": email})

        if result.fetchone() is not None:
            flash("Email id already exists. Try logging in or try registerting with other email id.")
            return render_template("/auth/register.html")
        
        
        
        if User.query.count() == 0:
            new = User(username,"admin",email,password)
            db.session.add(new)
            db.session.commit()

            adminNew = Admin(name,username,email,password,"admin")
            db.session.add(adminNew)
            db.session.commit()

            flash("Admin user created.")
            return redirect(url_for('login'))
            
            

        try:
            userType = request.form["userType"]
        except KeyError:
            flash("Select the user type: Influencer OR Sponsor.")
            return redirect(url_for('register'))
            
        userType = request.form["userType"]
        session["userType"] = userType
        
        if userType == "influencer":
            new = User(username,userType,email,password)
            db.session.add(new)
            db.session.commit()


            influencerNew = Influencer(name,username,email,password,userType,"","")
            db.session.add(influencerNew)
            db.session.commit()

            flash("Add details to continue.")
            return redirect(url_for('influencerDetails'))
            


        elif userType == "sponsor":
            new = User(username,userType,email,password)
            db.session.add(new)
            db.session.commit()


            sponsorNew = Sponsor(name,username,email,password,userType,0)
            db.session.add(sponsorNew)
            db.session.commit()


            flash("Add details to continue.")
            return redirect(url_for('sponsorDetails'))
            


        else:
            flash("Choose the user type : Influencer or Sponsor.")
            return render_template("/auth/register.html")

        
    return render_template('/auth/register.html')


@app.route('/logout')
def logout():
    with db.engine.begin() as connection:
        query = text("UPDATE user SET isActive = 0 WHERE username = :username")
        details = {"username" : session["username"]}
        connection.execute(query,details)
    logout_user()
    session.pop('username', None)
    flash("Logged out. Log in again to continue.")
    return redirect(url_for('login'))
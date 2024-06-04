from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user

from application.models.user import User


@app.route("/admin/dashboard",methods=["GET","POST"])
@login_required
def adminDashboard():
    username = session["username"]

    with db.engine.begin() as connection:
        query = text("SELECT userType FROM user WHERE username = :username")
        result = connection.execute(query,{"username":username})
        row = result.fetchone()
        if row[0] == "sponsor":
            return redirect(url_for('sponsorDashboard'))
        elif row[0] == "influencer":
            return redirect(url_for("influencerDashboard"))
        else:
            pass

    if request.method == "POST":
        return "bye"
    
    return render_template("admin/dashboard.html",username=username)
    

@app.route("/admin/user_management",methods=["GET","POST"])
@login_required
def userManagement():

    connection = db.engine.connect()
    query = text("SELECT * FROM user ORDER BY username")
    result = connection.execute(query)
    users = result.fetchall()
    

    if request.method =="POST":
        try:
            username = request.form["usernameSearch"]
            
            try:
                query = text("SELECT * FROM user WHERE username = :username OR username LIKE :show ORDER BY username")
                result = connection.execute(query,{"username":username, "show": f"%{username}%"})
                rows = result.fetchall()
                if rows is None:
                    flash("No user found. Please check again.")
                    return render_template("admin/userManagement.html",users=users,username=session["username"])
                return render_template("admin/userManagement.html",users=rows,username=session["username"])

            except Exception as e:
                flash(f"Error occurred: {e}")
                return render_template("admin/userManagement.html",users=users,username=session["username"])


        except KeyError:
            filterbychoice = request.form["filterbychoice"]
            filterbyvalue = request.form["filterbyvalue"] 

            try:
                if filterbychoice =="isActive":
                    if filterbyvalue == "active":
                        filterbyvalue = 1
                    else:
                        filterbyvalue = 0
                    query = text("SELECT * FROM user WHERE isActive = :filterbyvalue ORDER BY username")
                    details = {"filterbyvalue" :filterbyvalue }
                    result = connection.execute(query,details)
                    rows = result.fetchall()
                
                    if rows is None:
                        flash("No user found. Please check again.")
                        return render_template("admin/userManagement.html",users=users,username=session["username"])
                    
                elif filterbychoice =="isflagged":
                    if filterbyvalue == "not flagged":
                        filterbyvalue = 0
                    else:
                        filterbyvalue = 1
                    query = text("SELECT * FROM user WHERE isflagged = :filterbyvalue ORDER BY username")
                    details = {"filterbyvalue" :filterbyvalue }
                    result = connection.execute(query,details)
                    rows = result.fetchall()
                
                    if rows is None:
                        flash("No user found. Please check again.")
                        return render_template("admin/userManagement.html",users=users,username=session["username"])

                else:
                    query = text("SELECT * FROM user WHERE userType = :filterbyvalue ORDER BY username")
                    details = {"filterbyvalue" :filterbyvalue }
                    result = connection.execute(query,details)
                    rows = result.fetchall()
                
                    if rows is None:
                        flash("No user found. Please check again.")
                        return render_template("admin/userManagement.html",users=users,username=session["username"])
                    
                
                return render_template("admin/userManagement.html",users=rows,username=session["username"])

            except Exception as e:
                flash(f"Error occurred: {e}")
                return render_template("admin/userManagement.html",users=users,username=session["username"])
    

    if request.method == "GET":
        return render_template("admin/userManagement.html",users=users,username=session["username"])
    

@app.route("/admin/flag_user/<username>",methods=["GET"])
def flagUser(username):
    query = text("UPDATE user SET isflagged = 1 WHERE username = :username")
    details = {"username":username}
    with db.engine.begin() as conn:
        conn.execute(query,details)
        query = text("SELECT * FROM user")
        result = conn.execute(query)

        users = result.fetchall()
        return redirect(url_for("userManagement"))
    



@app.route("/admin/unflag_user/<username>")
def unflagUser(username):
    query = text("UPDATE user SET isflagged = 0 WHERE username = :username")
    details = {"username":username}
    with db.engine.begin() as conn:
        conn.execute(query,details)
        query = text("SELECT * FROM user")
        result = conn.execute(query)

        users = result.fetchall()
        return redirect(url_for("userManagement"))


@app.route("/admin/addUser",methods = ["GET","POST"])
def addUser():
    
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
            return render_template("/admin/addUser.html",username=session["username"])
        
        connection = db.engine.connect()
        query = text("SELECT email FROM user WHERE email = :email")
        result = connection.execute(query,{"email": email})

        if result.fetchone() is not None:
            flash("Email id already exists.")
            return render_template("/admin/addUser.html",username=session["username"])
            

        try:
            userType = request.form["userType"]
            
            new = User(username,userType,email,password)
            db.session.add(new)
            db.session.commit()

            flash("User added successfully! Click on User Management to see.")
            return render_template("/admin/addUser.html",username=session["username"])
        
        except KeyError:
            
            flash("Select the user type: Admin OR Influencer OR Sponsor.")
            return render_template("/admin/addUser.html",username=session["username"])
        
        
    return render_template("/admin/addUser.html",username=session["username"])

from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for,jsonify
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user

from application.models.user import *


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
                    return render_template("admin/userManagement.html",users=users,username=session["username"],method="GET")
                return render_template("admin/userManagement.html",users=rows,username=session["username"],method="GET")

            except Exception as e:
                flash(f"Error occurred: {e}")
                return render_template("admin/userManagement.html",users=users,username=session["username"],method="GET")


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
                        return render_template("admin/userManagement.html",users=users,username=session["username"],method="GET")
                    
                    return render_template("admin/userManagement.html",users=rows,username=session["username"],method="GET")
                    
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
                        return render_template("admin/userManagement.html",users=users,username=session["username"],method="GET")
                    
                    return render_template("admin/userManagement.html",users=rows,username=session["username"],method="GET")

                else:
                    query = text("SELECT * FROM user WHERE userType = :filterbyvalue ORDER BY username")
                    details = {"filterbyvalue" :filterbyvalue }
                    result = connection.execute(query,details)
                    rows = result.fetchall()
                
                    if rows is None:
                        flash("No user found. Please check again.")
                        return render_template("admin/userManagement.html",users=users,username=session["username"],method="GET")
                    
                    return render_template("admin/userManagement.html",users=rows,username=session["username"],method="GET")

            except Exception as e:
                flash(f"Error occurred: {e}")
                return render_template("admin/userManagement.html",users=users,username=session["username"],method="GET")
    

    if request.method == "GET":
        return render_template("admin/userManagement.html",users=users,username = session["username"])
    

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

            if userType == "admin":
                new = Admin(name,username,email,password,userType)
                db.session.add(new)
                db.session.commit()

            elif userType == "influencer":
                new = Influencer(name,username,email,password,userType,"","")
                db.session.add(new)
                db.session.commit()

            else:
                new = Sponsor(name,username,email,password,userType,0)
                db.session.add(new)
                db.session.commit()



            flash("User added successfully! Click on User Management to see.")
            return render_template("/admin/addUser.html",username=session["username"])
        
        except KeyError:
            
            flash("Select the user type: Admin OR Influencer OR Sponsor.")
            return render_template("/admin/addUser.html",username=session["username"])
        
        
    return render_template("/admin/addUser.html",username=session["username"])


@app.route("/admin/settings",methods=["GET","POST"])
def adminSettings():



    with db.engine.begin() as connection:
        query = text("SELECT admin.name,user.username,user.email FROM user JOIN admin ON user.username = admin.username WHERE user.username = :username")
        details = {"username": session["username"]}

        results = connection.execute(query,details)

        userDetails = results.fetchall()

        if userDetails is None:
            flash("No user found!")
            return render_template("/admin/settings.html",username=session["username"])
        

    if request.method == "POST":

        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]


        with db.engine.begin() as connection:

            orignalUN = session["username"]
            
            if username != orignalUN:
                query = text("SELECT username FROM user WHERE username = :username")
                details = {"username":username}

                results = connection.execute(query,details)
            

                if results.fetchall() != []:
                    flash("Username already exists. Try another username.")
                    return render_template("/admin/settings.html",username=session["username"],userDetails = userDetails[0],method="GET")
            
            query = text("SELECT email FROM user WHERE username = :user")
            details = {"user":session["username"]}

            results = connection.execute(query,details)

            orignalEM = results.fetchall()[0][0]

            if email!= orignalEM:
            
                query = text("SELECT email FROM user WHERE email = :email")
                details = {"email":email}

                results = connection.execute(query,details)

            

                if results.fetchall() != []:
                    flash("Email already exists. Try another email.")
                    return render_template("/admin/settings.html",username=session["username"],userDetails = userDetails[0],method="GET")


            query = text("UPDATE user SET username = :username, email = :email WHERE username = :user")
            details = {"username":username,"email":email,"user" :session["username"]}

            connection.execute(query,details)

            query = text("UPDATE admin SET username = :username, email = :email, name = :name WHERE username = :user")
            details = {"name":name,"username":username,"email":email,"user" :session["username"]}

            connection.execute(query,details)

            flash("User details edited!")

            query = text("SELECT admin.name,user.username,user.email FROM user JOIN admin ON user.username = admin.username WHERE user.username = :username")
            details = {"username": username}

            results = connection.execute(query,details)

            userDetails = results.fetchall()

            session["username"] = username


            return render_template("/admin/settings.html",username=session["username"],userDetails = userDetails[0],method="GET")
    

    return render_template("admin/settings.html",userDetails = userDetails[0],username = session["username"])


@app.route("/admin/see_user_details/<username>")
def see_user_details(username):


    with db.engine.connect() as connection:
        query = text("SELECT userType FROM user WHERE username = :username")
        details = {"username": username}

        results = connection.execute(query,details)

        row = results.fetchone()
        
        if row[0] == "admin":

            query = text("SELECT * FROM admin WHERE username = :username")
            details = {"username": username}
            results = connection.execute(query,details)
            userDetails = results.fetchone()
            return f"{userDetails}"


            return "admin"
        
        if row[0] == "influencer":

            query = text("SELECT * FROM influencer WHERE username = :username")
            details = {"username": username}
            results = connection.execute(query,details)
            userDetails = results.fetchone()
            return f"{userDetails}"

            return "influencer"
        
        if row[0] == "sponsor":

            query = text("SELECT * FROM sponsor WHERE username = :username")
            details = {"username": username}
            results = connection.execute(query,details)
            userDetails = results.fetchone()
            
            return f"{userDetails}"
            return "sponsor"

    return render_template("admin/user_details.html")

@app.route("/admin/delete_user/<username>")
def deleteUser(username):
    
    if username != session["username"]:
        with db.engine.connect() as connection:
            query = text("SELECT isActive FROM user WHERE username = :username")
            details = {"username": username}

            results = connection.execute(query,details)
            row = results.fetchone()

            
            if row[0] == 1:
                flash("You cannot delete user when the user is active.")
                return redirect(url_for("userManagement"))
            
            else:
                query = text("SELECT userType FROM user WHERE username= :username")
                details = {"username": username}

                results = connection.execute(query,details)

                userType = results.fetchone()[0]

                user = User.query.filter_by(username=username).first()
                db.session.delete(user)
                db.session.commit()
                

                if userType == "admin":
                    user = Admin.query.filter_by(username=username).first()
                    db.session.delete(user)
                    db.session.commit()
                elif userType=="influencer":
                    user = Influencer.query.filter_by(username=username).first()
                    db.session.delete(user)
                    db.session.commit()
                else:
                    user = Sponsor.query.filter_by(username=username).first()
                    db.session.delete(user)
                    db.session.commit()

            flash("User deleted successfully!")
            return redirect(url_for("userManagement"))

    else:
        flash("You cannot delete the user as you are logged in! Please check settings to delete account.")
        return redirect(url_for("userManagement"))
        
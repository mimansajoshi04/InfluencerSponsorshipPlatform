from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user


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
    
    return render_template("admin/dashboard.html")
    

@app.route("/admin/user_management",methods=["GET","POST"])
def userManagement():

    if request.method =="POST":


        return


    connection = db.engine.connect()
    query = text("SELECT * FROM user")
    result = connection.execute(query)

    users = result.fetchall()
    
    return render_template("admin/userManagement.html",users=users)
from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user


@app.route('/sponsor/getDetails',methods=["GET","POST"])
def sponsorDetails():
    if request.method == "POST":

        username = session["username"]
        industry = request.form["industry"]
        budget = request.form["budget"]

        details = {"username": username,"industry": industry,"budget": int(budget)}

        try:
            with db.engine.begin() as connection:
                query = text("UPDATE sponsor SET industry = :industry, budget = :budget WHERE username = :username")
                connection.execute(query,details)
            db.engine.dispose()
            flash("Registered succesfully. Login to continue.")
            return redirect(url_for('login'))
        
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('sponsorDetails'))

        return "hi"
    
    industry=["Aerospace","Automotive","Education","Energy","Entertainment","Finance","Healthcare","Hospitality","Retail","Technology","Telecommunications"]
    return render_template("/sponsor/getDetails.html",industry=industry)


@app.route('/sponsor/dashboard',methods=["GET","POST"])
@login_required
def sponsorDashboard():
    username = session["username"]

    with db.engine.begin() as connection:
        query = text("SELECT userType FROM user WHERE username = :username")
        result = connection.execute(query,{"username":username})
        row = result.fetchone()
        if row[0] == "influencer":
            return redirect(url_for('influencerDashboard'))
        elif row[0] == "admin":
            return redirect(url_for("adminDashboard"))
        else:
            pass

    if request.method == "POST":
        return "bye"
    
    return "hi"
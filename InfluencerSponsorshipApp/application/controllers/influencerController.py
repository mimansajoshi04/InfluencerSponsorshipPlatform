from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user


@app.route('/influencer/getDetails',methods=["GET","POST"])
def influencerDetails():


    if request.method=="POST":
        
        username = session["username"]

        
        category = request.form["category"]
        niche = request.form["niche"]
        followers = request.form["followers"]
        instaid = request.form["insta_id"]

        details = {"category": category, "niche": niche, "followers":followers, "instaid": instaid, "username" : username}
        
        
        try:
            with db.engine.begin() as connection:
                query = text("UPDATE influencer SET category = :category, niche = :niche, followers = :followers, instaid = :instaid WHERE username = :username")
                connection.execute(query, details)
            db.engine.dispose()
            flash("Registered successfully. Login to continue.")
            return redirect(url_for('login'))

        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('influencerDetails'))
        
    
    
    category = ["Arts and Entertainment","Business","Designer","Education","Fashion and Beauty","Finance","Health and Wellness","Public Figure","Technology","Travel"]
    return render_template("influencer/getDetails.html",category=category)
    


    

@app.route('/influencer/dashboard',methods=["GET","POST"])
@login_required
def influencerDashboard():
    username = session["username"]

    with db.engine.begin() as connection:
        query = text("SELECT userType FROM user WHERE username = :username")
        result = connection.execute(query,{"username":username})
        row = result.fetchone()
        if row[0] == "sponsor":
            return redirect(url_for('sponsorDashboard'))
        elif row[0] == "admin":
            return redirect(url_for("adminDashboard"))
        else:
            pass

    if request.method == "POST":
        return "bye"
    
    return "hi"
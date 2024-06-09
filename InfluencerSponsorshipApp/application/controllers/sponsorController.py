from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user

from application.models.user import User,Sponsor
from application.models.messages import *

@app.route("/sponsor/send_message",methods=["GET","POST"])
@login_required
def sendSMessage():
    if request.method =="POST":
        reciever = request.form["username"]

        with db.engine.begin() as connection:
            query = text("SELECT username FROM user WHERE username = :username")
            details = {"username":reciever}
            results = connection.execute(query,details)
            if results.fetchone() is None:
                flash("User does not exist.")
                return redirect(url_for("sendAMessage"))


        title = request.form["title"]
        message = request.form["message"]
        sent_by = session["username"]

        time = datetime.now()


        message = Message(title,message,sent_by,reciever,time,"sent",-1)
        db.session.add(message)
        db.session.commit()

        
        with db.engine.begin() as connection:
            query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
            details = {"username":reciever}
            connection.execute(query,details)

        flash("Message has been sent!")
        return redirect(url_for("sponsorMessages"))

    return render_template("/sponsor/send_message.html",username=session["username"])

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
        query = text("SELECT userType,isflagged,newMessages FROM user WHERE username = :username")
        result = connection.execute(query,{"username":username})
        row = result.fetchone()

        
        if row[0] == "influencer":
            return redirect(url_for('influencerDashboard'))
        elif row[0] == "admin":
            return redirect(url_for("adminDashboard"))
        else:
            pass

    if request.method == "POST":

        username = request.form["username"]
        complain = request.form["complain"]

        time = datetime.now()
        

        with db.engine.begin() as connection:
            query = text("SELECT username FROM user WHERE userType = :userType")
            details = {"userType":"admin"}

            results = connection.execute(query,details)
            rows = results.fetchall()

        
            
        for r in rows:
            adminUsername = r[0]

            message = Message("User Flagged Request",complain,username,adminUsername,time,"sent",-1)
            db.session.add(message)
            db.session.commit()

        
            with db.engine.begin() as connection:
                query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
                details = {"username":adminUsername}
                connection.execute(query,details)




        return render_template("sponsor/dashboard.html",username = session["username"],flagged=row[1],new=row[2],method="GET")
    
    return render_template("sponsor/dashboard.html",username = session["username"],flagged=row[1],new=row[2])

@app.route("/sponsor/settings",methods=["GET","POST"])
def sponsorSettings():
     
    with db.engine.begin() as connection:
        query = text("SELECT sponsor.companyName,user.username,user.email,sponsor.industry,sponsor.budget,user.isflagged FROM user JOIN sponsor ON user.username = sponsor.username WHERE user.username = :username")
        details = {"username": session["username"]}
        results = connection.execute(query,details)
        userDetails = results.fetchall()

        query=text("SELECT newMessages FROM user WHERE username = :username")
        results=connection.execute(query,details)
        row=results.fetchone()

        if userDetails is None:
            flash("No user found!")
            return render_template("/sponsor/settings.html",username=session["username"],new=row[0])
        
    indus=["Aerospace","Automotive","Education","Energy","Entertainment","Finance","Healthcare","Hospitality","Retail","Technology","Telecommunications"]
        

    if request.method == "POST":
        try:
            name = request.form["name"]
            username = request.form["username"]
            email = request.form["email"]
            industry = request.form["industry"]
            budget = request.form["budget"]


            with db.engine.begin() as connection:

                orignalUN = session["username"]
            
                if username != orignalUN:
                    query = text("SELECT username FROM user WHERE username = :username")
                    details = {"username":username}

                    results = connection.execute(query,details)
            

                    if results.fetchall() != []:
                        flash("Username already exists. Try another username.")
                        return render_template("/sponsor/settings.html",username=session["username"],userDetails = userDetails[0],new=row[0],method="GET")
            
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
                        return render_template("/sponsor/settings.html",username=session["username"],userDetails = userDetails[0],new=row[0],method="GET")


                query = text("UPDATE user SET username = :username, email = :email WHERE username = :user")
                details = {"username":username,"email":email,"user" :session["username"]}

                connection.execute(query,details)

                query = text("UPDATE sponsor SET username = :username, email = :email, companyName = :companyName, budget = :budget, industry = :industry WHERE username = :user")
                details = {"companyName":name,"username":username,"email":email,"user" :session["username"],"budget":budget,"industry":industry}

                connection.execute(query,details)

                flash("User details edited!")

                query = text("SELECT sponsor.companyName,user.username,user.email,sponsor.industry,sponsor.budget,user.isflagged FROM user JOIN sponsor ON user.username = sponsor.username WHERE user.username = :username")
                details = {"username": username}

                results = connection.execute(query,details)

                userDetails = results.fetchall()

                session["username"] = username


                return render_template("/sponsor/settings.html",username=session["username"],userDetails = userDetails[0],industry=indus,flagged=userDetails[0][5],new=row[0],method="GET")
            
        except KeyError:
            username = request.form["username"]
            complain = request.form["complain"]

            time = datetime.now()
        

            with db.engine.begin() as connection:
                query = text("SELECT username FROM user WHERE userType = :userType")
                details = {"userType":"admin"}

                results = connection.execute(query,details)
                rows = results.fetchall()

        
            
            for r in rows:
                adminUsername = r[0]

                message = Message("User Flagged Request",complain,username,adminUsername,time,"sent",-1)
                db.session.add(message)
                db.session.commit()

        
                with db.engine.begin() as connection:
                    query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
                    details = {"username":adminUsername}
                    connection.execute(query,details)

            flash("Complain has been sent!")
            return redirect(url_for("sponsorSettings"))
    

    return render_template("/sponsor/settings.html",username=session["username"],userDetails = userDetails[0],industry=indus,flagged=userDetails[0][5],new=row[0])


@app.route("/sponsor/delete_account")
def deleteSponsorAccount():

    username = session["username"]
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    user = Sponsor.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    
    flash(f"User {username} has been permanantly deleted.")
    logout_user()

    return redirect(url_for("login"))


@app.route("/sponsor/mark_as_read/<id>")
def markAsReadS(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 1 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("adminMessages"))

@app.route("/sponsor/mark_as_unread/<id>")
def markAsUnreadS(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 0 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("adminMessages"))

@app.route("/sponsor/reply/<int:id>/<reciever>",methods=["GET","POST"])
@login_required
def sponsorreply(id,reciever):
    
    if request.method=="POST":
        title = request.form["title"]
        message = request.form["message"]
        sent_by = session["username"]

        time = datetime.now()


        message = Message(title,message,sent_by,reciever,time,"reply",id)
        db.session.add(message)
        db.session.commit()

        
        with db.engine.begin() as connection:
            query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
            details = {"username":reciever}
            connection.execute(query,details)

        flash("Message has been sent!")
        return redirect(url_for("sponsorMessages"))
    else:
        return render_template("sponsor/replyMessage.html",username=session["username"])
#
@app.route('/sponsor/messages')
@login_required
def sponsorMessages():

    with db.engine.begin() as connection:
        query = text("SELECT * FROM message WHERE sent_to = :username OR sent_by = :username ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        all = results.fetchall()

        query = text("SELECT * FROM message WHERE sent_to = :username AND read = 1 ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        read = results.fetchall()

        query = text("SELECT * FROM message WHERE sent_to = :username AND read = 0 ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        unread = results.fetchall()

        query = text("SELECT * FROM message WHERE sent_by = :username ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        sent = results.fetchall()

    if unread == []:
        with db.engine.begin() as connection:
            query = text("UPDATE user SET newMessages = 0 WHERE username = :username ")
            details = {"username":session["username"]}
            connection.execute(query,details)

    else:
        with db.engine.begin() as connection:
            query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
            details = {"username":session["username"]}
            connection.execute(query,details)
    
    return render_template("sponsor/messages.html",all=all,read=read,unread=unread,username = session["username"],sent=sent)
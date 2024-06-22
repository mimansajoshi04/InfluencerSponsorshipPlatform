from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for,jsonify
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user

from application.models.user import *
from application.models.messages import *


@app.route("/admin/dashboard",methods=["GET","POST"])
@login_required
def adminDashboard():
    username = session["username"]

    with db.engine.begin() as connection:
        query = text("SELECT userType,newMessages FROM user WHERE username = :username")
        result = connection.execute(query,{"username":username})
        row = result.fetchone()
        if row[0] == "sponsor":
            return redirect(url_for('sponsorDashboard'))
        elif row[0] == "influencer":
            return redirect(url_for("influencerDashboard"))
        else:
            pass

        
    
    return render_template("admin/dashboard.html",username=username,new=row[1])
    

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
        with db.engine.begin() as connection:
            query = text("SELECT newMessages FROM user WHERE username = :user")
            details = {"user":session["username"]}
            results = connection.execute(query,details)
            row = results.fetchone()

            return render_template("admin/userManagement.html",users=users,username = session["username"],new=row[0])
    

@app.route("/admin/flag_user/<username>",methods=["GET"])
@login_required
def flagUser(username):
    query = text("UPDATE user SET isflagged = 1 WHERE username = :username")
    details = {"username":username}
    with db.engine.begin() as conn:
        conn.execute(query,details)
        query = text("SELECT * FROM user")
        result = conn.execute(query)

        users = result.fetchall()
        return redirect(url_for("userManagement"))
    
@app.route("/admin/campaigns",methods=["GET","POST"])
@login_required
def seeCampaigns():

    with db.engine.begin() as connection:

        query = text("SELECT newMessages FROM user WHERE username = :user")
        details = {"user":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        query = text("SELECT * FROM campaign ORDER BY name")
        results = connection.execute(query)
        all = results.fetchall()


    if request.method =="POST":
        
        try:
            name = request.form["name"]

            try:
                with db.engine.begin() as connection:
                    query = text("SELECT * FROM campaign WHERE (name = :name OR name LIKE :show) ORDER BY name")
                    result = connection.execute(query,{"name":name, "show": f"%{name}%"})
                    rows = result.fetchall()
                    if rows is None:
                        flash("No campaign found. Please check again.")
                        return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                    return render_template("admin/campaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
            except Exception as e:
                flash(f"Error occurred: {e}")
                return render_template("admin/campigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
        
        except KeyError:
            try:
                niche = request.form["n"]
                try:
                    with db.engine.begin() as connection:
                        query = text("SELECT * FROM campaign WHERE (niche = :n OR niche LIKE :show) ORDER BY name")
                        result = connection.execute(query,{"n":niche, "show": f"%{niche}%"})
                        rows = result.fetchall()
                        if rows is None:
                            flash("No campaign found. Please check again.")
                            return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                        return render_template("admin/campaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                except Exception as e:
                    flash(f"Error occurred: {e}")
                    return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                
            except KeyError:
                filterbychoice = request.form["filterbychoice"]
                filterbyvalue = request.form["filterbyvalue"] 

                try:
                    if filterbychoice =="visibility":
                        if filterbyvalue == "public":
                            filterbyvalue = "public"
                        else:
                            filterbyvalue = "private"
                        with db.engine.begin() as connection:
                            query = text("SELECT * FROM campaign WHERE visibility = :filterbyvalue ORDER BY name")
                            details = {"filterbyvalue" :filterbyvalue}
                            result = connection.execute(query,details)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No campaign found. Please check again.")
                                return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("admin/campaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                        
                    elif filterbychoice =="isflagged":
                        if filterbyvalue == "not flagged":
                            filterbyvalue = 0
                        else:
                            filterbyvalue = 1
                        with db.engine.begin() as connection:
                            query = text("SELECT * FROM campaign WHERE isflagged = :filterbyvalue ORDER BY name")
                            details = {"filterbyvalue" :filterbyvalue}
                            result = connection.execute(query,details)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No campaign found. Please check again.")
                                return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("admin/campaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                        
                    elif filterbychoice =="status":
                        date=datetime.now()
                        if filterbyvalue == "on going":
                            query = text(f"SELECT * FROM campaign WHERE end_date > '{date}' AND start_date < '{date}'  ORDER BY name")
                        
                        elif filterbyvalue == "scheduled":
                            query = text(f"SELECT * FROM campaign WHERE start_date > '{date}' ORDER BY name")
                        
                        else:
                            query = text(f"SELECT * FROM campaign WHERE end_date < '{date}' ORDER BY name")
                        with db.engine.begin() as connection:
                            
                            result = connection.execute(query)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No campaign found. Please check again.")
                                return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("admin/campaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")


                    else:
                        with db.engine.begin() as connection:
                            query = text("SELECT * FROM campaign WHERE category = :filterbyvalue ORDER BY name")
                            details = {"filterbyvalue" :filterbyvalue}
                            result = connection.execute(query,details)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No user found. Please check again.")
                                return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("admin/campaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")

                except Exception as e:
                    flash(f"Error occurred: {e}")
                    return render_template("admin/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")




    return render_template("admin/campaigns.html",username=session["username"],new=row[0],campaigns = all)


@app.route("/admin/unflag_user/<username>")
@login_required
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
@login_required
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
            return redirect(url_for("addUser"))
        
        connection = db.engine.connect()
        query = text("SELECT email FROM user WHERE email = :email")
        result = connection.execute(query,{"email": email})

        if result.fetchone() is not None:
            flash("Email id already exists.")
            return redirect(url_for("addUser"))
            

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
            return redirect(url_for("addUser"))
        
        except KeyError:
            
            flash("Select the user type: Admin OR Influencer OR Sponsor.")
            return redirect(url_for("addUser"))
        
    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :user")
        details = {"user":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()
        
        return render_template("/admin/addUser.html",username=session["username"],new=row[0])


@app.route("/admin/settings",methods=["GET","POST"])
@login_required
def adminSettings():



    with db.engine.begin() as connection:
        query = text("SELECT admin.name,user.username,user.email FROM user JOIN admin ON user.username = admin.username WHERE user.username = :username")
        details = {"username": session["username"]}

        results = connection.execute(query,details)

        userDetails = results.fetchall()

        query = text("SELECT newMessages FROM user WHERE username = :user")
        details = {"user":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        if userDetails is None:
            flash("No user found!")
            return redirect(url_for("addUser"))
        

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
                    return redirect(url_for("adminSettings"))
            
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
                    return redirect(url_for("adminSettings"))


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

            query = text("SELECT newMessages FROM user WHERE username = :user")
            details = {"user":session["username"]}
            results = connection.execute(query,details)
            row = results.fetchone()


            return render_template("/admin/settings.html",username=session["username"],userDetails = userDetails[0],new = row[0],method="GET")
    

    return render_template("admin/settings.html",userDetails = userDetails[0],new = row[0],username = session["username"])


@app.route("/admin/see_user_details/<username>")
@login_required
def see_user_details(username):


    with db.engine.connect() as connection:
        query = text("SELECT userType,newMessages FROM user WHERE username = :username")
        details = {"username": username}

        results = connection.execute(query,details)

        row = results.fetchone()
        
        
        if row[0] == "admin":

            query = text("SELECT * FROM admin WHERE username = :username")
            details = {"username": username}
            results = connection.execute(query,details)
            userDetails = results.fetchone()
            
            return render_template("admin/user_details.html",userDetails=userDetails,username=session["username"],new=row[1],userType="admin")
        
        if row[0] == "influencer":

            query = text("SELECT * FROM influencer WHERE username = :username")
            details = {"username": username}
            results = connection.execute(query,details)
            userDetails = results.fetchone()
            
            return render_template("admin/user_details.html",userDetails=userDetails,username=session["username"],new=row[1],userType="influencer")
        
        if row[0] == "sponsor":

            query = text("SELECT * FROM sponsor WHERE username = :username")
            details = {"username": username}
            results = connection.execute(query,details)
            userDetails = results.fetchone()
            
            return render_template("admin/user_details.html",userDetails=userDetails,username=session["username"],new=row[1],userType="sponsor")

    return render_template("admin/user_details.html")

@app.route("/admin/delete_user/<username>")
@login_required
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
        

@app.route("/admin/delete_account")
@login_required
def deleteAdminAccount():

    with db.engine.begin() as connection:
        query = text("SELECT count(*) FROM user WHERE userType = 'admin'")
        results = connection.execute(query)
        count = results.fetchone()

        if count[0]==1:
            flash("This is the only admin account currently present. Deletion not allowed.")
            return redirect(url_for("adminSettings"))

        
    username =session["username"]
    session.pop("username",None)

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    user = Admin.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    
    flash(f"User {username} has been permanantly deleted.")
    logout_user()

    return redirect(url_for("login"))

    
@app.route('/admin/messages')
@login_required
def adminMessages():

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

        query = text(f"SELECT * FROM report WHERE report_type = 'user' ORDER BY id DESC")
        results = connection.execute(query)

        userReports = results.fetchall()

        

        query = text("SELECT * FROM report WHERE report_type = 'campaign' ORDER BY id DESC")
        results = connection.execute(query)

        campaignReports = results.fetchall()


    if unread == []:
        with db.engine.begin() as connection:
            query = text("UPDATE user SET newMessages = 0 WHERE username = :username")
            details = {"username":session["username"]}
            connection.execute(query,details)

    else:
        with db.engine.begin() as connection:
            query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
            details = {"username":session["username"]}
            connection.execute(query,details)
    
    return render_template("admin/adminMessages.html",all=all,read=read,unread=unread,sent = sent,userReports=userReports,campaignReports=campaignReports,username = session["username"])

@app.route("/admin/mark_as_read/<id>")
def markAsReadA(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 1 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("adminMessages"))

@app.route("/admin/mark_as_unread/<id>")
def markAsUnreadA(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 0 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("adminMessages"))

@app.route("/admin/send_message",methods=["GET","POST"])
@login_required
def sendAMessage():

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
        return redirect(url_for("adminMessages"))

    return render_template("/admin/send_message.html",username=session["username"])

@app.route("/admin/reply/<int:id>/<reciever>",methods=["GET","POST"])
@login_required
def adminreply(id,reciever):

    
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
        return redirect(url_for("adminMessages"))
    else:
        return render_template("admin/replyMessage.html",username=session["username"])
    

#hi
@app.route("/admin/adRequests",methods=["GET","POST"])
def adminAdRequests():
    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :username")
        details = {"username":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id")
        details = {"username":session["username"]}
        results = connection.execute(query,details)
        ads = results.fetchall()


    if request.method == "POST":
        try:
            start = request.form["start"]
            end = request.form["end"]

            with db.engine.begin() as connection:
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND ad.payment_amount >{int(start)} AND ad.payment_amount< {int(end)} ")
                details = {"username":session["username"]}
                results = connection.execute(query,details)
                a = results.fetchall()

            return render_template("admin/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")

        except:

            filterbychoice = request.form["filterbychoice"]
            filterbyvalue = request.form["filterbyvalue"]

            if filterbychoice=="category":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.category = '{filterbyvalue}' ")

            elif filterbychoice == "visibility":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.visibility = '{filterbyvalue}' ")

            elif filterbychoice == "status":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND ad.status = '{filterbyvalue}' ")
            
            elif filterbychoice == "deleted":
                if filterbyvalue == "deleted":
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND ad.deleted = 1 ")
                else:
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND ad.deleted = 0 ")


            else:
                if filterbyvalue == "flagged":
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.isflagged = 1 ")
                else:
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.isflagged = 0 ")

            with db.engine.begin() as connection:
                result = connection.execute(query)
                a = result.fetchall()

            return render_template("admin/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")


    return render_template("admin/adRequests.html",username=session["username"],new=row[0],ads=ads)



@app.route("/admin/flag_campaign/<int:id>",methods=["GET"])
@login_required
def flagCampaign(id):
    query = text("UPDATE campaign SET isflagged = 1 WHERE id = :id")
    details = {"id":id}
    with db.engine.begin() as conn:
        conn.execute(query,details)
        return redirect(url_for("seeCampaigns"))
    
@app.route("/admin/unflag_campaign/<int:id>",methods=["GET"])
@login_required
def unflagCampaign(id):
    query = text("UPDATE campaign SET isflagged = 0,reports=0 WHERE id = :id")
    details = {"id":id}
    with db.engine.begin() as conn:
        conn.execute(query,details)
        return redirect(url_for("seeCampaigns"))
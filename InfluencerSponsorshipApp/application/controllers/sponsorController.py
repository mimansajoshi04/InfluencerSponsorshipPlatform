from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user

from application.models.user import User,Sponsor
from application.models.messages import *
from application.models.campaign import *
from application.models.adRequest import *

from application.controllers.auth import *

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
            complain = request.form["complain"]

            time = datetime.now()
        

            with db.engine.begin() as connection:
                query = text("SELECT username FROM user WHERE userType = :userType")
                details = {"userType":"admin"}

                results = connection.execute(query,details)
                rows = results.fetchall()

        
            
            for r in rows:
                adminUsername = r[0]

                message = Message("User Flagged Request",complain,session["username"],adminUsername,time,"sent",-1)
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
@login_required
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

    redirect(url_for("deleteCampaign",string="all"))

    return redirect(url_for("login"))


@app.route("/sponsor/mark_as_read/<id>")
def markAsReadS(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 1 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("sponsorMessages"))

@app.route("/sponsor/mark_as_unread/<id>")
def markAsUnreadS(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 0 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("sponsorMessages"))

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

@app.route("/sponsor/addCampaign",methods=["GET","POST"])
@login_required
def addSponsorCampaign():

    indus=["Aerospace","Automotive","Education","Energy","Entertainment","Finance","Healthcare","Hospitality","Retail","Technology","Telecommunications"]
    category = ["Arts and Entertainment","Business","Designer","Education","Fashion and Beauty","Finance","Health and Wellness","Public Figure","Technology","Travel"]

    with db.engine.begin() as connection:
        query = text("SELECT newMessages,isflagged FROM user WHERE username = :username")
        result = connection.execute(query,{"username":session["username"]})
        row = result.fetchone()

    if request.method=="POST":
        try:
            complain = request.form["complain"]

            time = datetime.now()
        

            with db.engine.begin() as connection:
                query = text("SELECT username FROM user WHERE userType = :userType")
                details = {"userType":"admin"}

                results = connection.execute(query,details)
                rows = results.fetchall()

        
            
            for r in rows:
                adminUsername = r[0]

                message = Message("User Flagged Request",complain,session["username"],adminUsername,time,"sent",-1)
                db.session.add(message)
                db.session.commit()

        
                with db.engine.begin() as connection:
                    query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
                    details = {"username":adminUsername}
                    connection.execute(query,details)

            flash("Complain has been sent!")
            return redirect(url_for("addSponsorCampaign"))

            

        except KeyError:
            
            name = request.form["name"]
            description = request.form["description"]
            budget = request.form["budget"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            visibility = request.form["visibility"]
            goals = request.form["goals"]
            category = request.form["category"]
            niche = request.form["join"]
            industry = request.form["industry"]

            date = start_date.split("-")
            start = datetime(int(date[0]),int(date[1]),int(date[2]))


            date = end_date.split("-")
            end = datetime(int(date[0]),int(date[1]),int(date[2]))

            

            with db.engine.begin() as connection:
                sponsor  = Campaign(name,description,start,end,session["username"],visibility,niche,category,goals,int(budget),industry)
                db.session.add(sponsor)
                db.session.commit()

            
            flash("New campaign created! Click on Campaign to see.")
            return render_template("sponsor/addCampaign.html",username=session["username"],industry=indus,category=category,new=row[0],flagged=row[1],method="GET")


    
    return render_template("sponsor/addCampaign.html",username=session["username"],industry=indus,category=category,new=row[0],flagged=row[1])


@app.route("/sponsor/my_campaigns",methods=["GET","POST"])
@login_required
def sponsorCampaigns():

    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :username")
        result = connection.execute(query,{"username":session["username"]})
        row = result.fetchone()

        query = text("SELECT * FROM campaign WHERE started_by=:username ORDER BY name")
        result = connection.execute(query,{"username":session["username"]})
        campaigns = result.fetchall()

    if request.method =="POST":
        try:
            name = request.form["name"]
            
            try:
                with db.engine.begin() as connection:
                    query = text("SELECT * FROM campaign WHERE (name = :name OR name LIKE :show) AND (started_by=:username) ORDER BY name")
                    result = connection.execute(query,{"name":name, "show": f"%{name}%","username":session["username"]})
                    rows = result.fetchall()
                    if rows is None:
                        flash("No campaign found. Please check again.")
                        return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                    return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
            except Exception as e:
                flash(f"Error occurred: {e}")
                return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")


        except KeyError:

            try:
                niche = request.form["n"]
                try:
                    with db.engine.begin() as connection:
                        query = text("SELECT * FROM campaign WHERE (niche = :n OR niche LIKE :show) AND (started_by=:username) ORDER BY name")
                        result = connection.execute(query,{"n":niche, "show": f"%{niche}%","username":session["username"]})
                        rows = result.fetchall()
                        if rows is None:
                            flash("No campaign found. Please check again.")
                            return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                        return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                except Exception as e:
                    flash(f"Error occurred: {e}")
                    return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")

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
                            query = text("SELECT * FROM campaign WHERE visibility = :filterbyvalue AND started_by=:username ORDER BY name")
                            details = {"filterbyvalue" :filterbyvalue,"username":session["username"]}
                            result = connection.execute(query,details)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No campaign found. Please check again.")
                                return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                        
                    elif filterbychoice =="isflagged":
                        if filterbyvalue == "not flagged":
                            filterbyvalue = 0
                        else:
                            filterbyvalue = 1
                        with db.engine.begin() as connection:
                            query = text("SELECT * FROM campaign WHERE isflagged = :filterbyvalue AND started_by=:username ORDER BY name")
                            details = {"filterbyvalue" :filterbyvalue,"username":session["username"]}
                            result = connection.execute(query,details)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No campaign found. Please check again.")
                                return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                        
                    elif filterbychoice =="status":
                        date=datetime.now()
                        if filterbyvalue == "on going":
                            query = text(f"SELECT * FROM campaign WHERE end_date > '{date}' AND started_by = '{session["username"]}' AND start_date < '{date}' ORDER BY name")
                        
                        elif filterbyvalue == "scheduled":
                            query = text(f"SELECT * FROM campaign WHERE start_date > '{date}' AND started_by = '{session["username"]}' ORDER BY name")
                        
                        else:
                            query = text(f"SELECT * FROM campaign WHERE end_date < '{date}' AND started_by = '{session["username"]}' ORDER BY name")
                        with db.engine.begin() as connection:
                            
                            result = connection.execute(query)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No campaign found. Please check again.")
                                return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")


                    else:
                        with db.engine.begin() as connection:
                            query = text("SELECT * FROM campaign WHERE category = :filterbyvalue AND started_by=:username ORDER BY name")
                            details = {"filterbyvalue" :filterbyvalue ,"username":session["username"]}
                            result = connection.execute(query,details)
                            rows = result.fetchall()
                    
                            if rows is None:
                                flash("No user found. Please check again.")
                                return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                        
                            return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")

                except Exception as e:
                    flash(f"Error occurred: {e}")
                    return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")


    return render_template("sponsor/myCampaigns.html",username=session["username"],new=row[0],campaigns=campaigns)


def deleteCampaign(string):

    if string =="all":
        with db.engine.begin() as connection:

            query = text("UPDATE ad SET deleted = 1 WHERE sponsor = :username")
            connection.execute(query,{"username":session["username"]})

            query = text("UPDATE campaign SET deleted = 1 WHERE started_by = :username")
            connection.execute(query,{"username":session["username"]})
            
        return
    else:
        with db.engine.begin() as connection:
            query = text("UPDATE ad SET deleted = 1 WHERE campaign_id = :id AND sponsor = :username")
            connection.execute(query,{"username": session["username"],"id":int(string)})

            
            query = text("UPDATE campaign SET deleted = 1 WHERE started_by = :username AND id = :id")
            connection.execute(query,{"username": session["username"],"id":int(string)})

            return


@app.route("/sponsor/ad_requests/<int:i>",methods=["GET","POST"])
def adSpons(i):
    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :username")
        details = {"username":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.campaign_id = {i} ")
        details = {"username":session["username"]}
        results = connection.execute(query,details)
        ads = results.fetchall()


    if request.method == "POST":
        try:
            start = request.form["start"]
            end = request.form["end"]

            with db.engine.begin() as connection:
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.payment_amount >{int(start)} AND ad.payment_amount< {int(end)} AND ad.campaign_id = {i} ")
                details = {"username":session["username"]}
                results = connection.execute(query,details)
                a = results.fetchall()

            return render_template("sponsor/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")

        except:

            filterbychoice = request.form["filterbychoice"]
            filterbyvalue = request.form["filterbyvalue"]

            if filterbychoice=="category":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.category = '{filterbyvalue}' AND ad.campaign_id = {i} ")

            elif filterbychoice == "visibility":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.visibility = '{filterbyvalue}' AND ad.campaign_id = {i} ")

            elif filterbychoice == "status":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.status = '{filterbyvalue}' AND ad.campaign_id = {i} ")
            
            elif filterbychoice == "deleted":
                if filterbyvalue == "deleted":
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.deleted = 1 AND ad.campaign_id = {i} ")
                else:
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.deleted = 0 AND ad.campaign_id = {i} ")


            else:
                if filterbyvalue == "flagged":
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.isflagged = 1 AND ad.campaign_id = {i} ")
                else:
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.isflagged = 0 AND ad.campaign_id = {i} ")

            with db.engine.begin() as connection:
                result = connection.execute(query)
                a = result.fetchall()

            return render_template("sponsor/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")


    return render_template("sponsor/adRequests.html",username=session["username"],new=row[0],ads=ads)


@app.route("/sponsor/find_influencers",methods=["GET","POST"])
@login_required
def find_influencers():

    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :username")
        result = connection.execute(query,{"username":session["username"]})
        row = result.fetchone()

        query = text("SELECT * FROM influencer ")
        result = connection.execute(query)
        influencers = result.fetchall()

    if request.method == "POST":
        user = request.form["complain_user"]
        complain = request.form["complain"]
        
        with db.engine.begin() as connection:

            query=text("UPDATE user SET reports = reports + 1 WHERE username= :username")
            result = connection.execute(query,{"username":user})

            query=text("SELECT reports FROM user WHERE username= :username")
            result = connection.execute(query,{"username":user})
            rows = result.fetchone()

            if rows[0]>3:
                query=text("UPDATE user SET isflagged = 1 WHERE username= :username")
                connection.execute(query,{"username":user})

        new = Report(complain,session["username"],user,datetime.now(),'user')
        db.session.add(new)
        db.session.commit()

        return render_template("sponsor/findInfluencer.html",new=row[0],username=session["username"],influencers=influencers,method="GET")
                


    return render_template("sponsor/findInfluencer.html",new=row[0],username=session["username"],influencers=influencers)


@app.route("/sponsor/delete_campaign/<int:id>",methods=["GET","POST"])
@login_required
def deleteSC(id):
    deleteCampaign(id)
    return redirect(url_for("sponsorCampaigns"))


@app.route("/sponsor/sendAdRequest/<string:influencer>/<string:sponsor>",methods=["GET","POST"])
@login_required
def sendAdRequest(influencer,sponsor):
    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :username")
        details = {"username":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        query = text(f"SELECT * FROM campaign WHERE started_by = '{session['username']}' AND deleted = 0")
        results = connection.execute(query)

        campaigns = results.fetchall()

    if sponsor != "-1":
        
        if request.method == "GET":
            return render_template("sponsor/getAdDetails.html",username=session["username"],new=row[0])

        else:

            name = request.form["name"]
            description = request.form["description"]
            amount = request.form["amount"]

            box = AdRequest(name,description,int(sponsor),influencer,session["username"],"pending",amount)
            db.session.add(box)
            db.session.commit()


            mess = Message("New Ad request!","New Ad request in the inbox!",session["username"],influencer,datetime.now(),"ad",-1)
            db.session.add(mess)
            db.session.commit()

            flash("Ad request is sent!")
            return redirect(url_for("sponsorAdRequests"))
    
    else:
        if request.method == "GET":
            return render_template("sponsor/newAdRequest.html",username=session["username"],new=row[0],campaigns=campaigns)
        
        else:
            try:
                name = request.form["name"]
                
                try:
                    with db.engine.begin() as connection:
                        query = text("SELECT * FROM campaign WHERE (name = :name OR name LIKE :show) AND (started_by=:username) ORDER BY name")
                        result = connection.execute(query,{"name":name, "show": f"%{name}%","username":session["username"]})
                        rows = result.fetchall()
                        if rows is None:
                            flash("No campaign found. Please check again.")
                            return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                        return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                except Exception as e:
                    flash(f"Error occurred: {e}")
                    return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")


            except KeyError:

                try:
                    niche = request.form["n"]
                    try:
                        with db.engine.begin() as connection:
                            query = text("SELECT * FROM campaign WHERE (niche = :n OR niche LIKE :show) AND (started_by=:username) ORDER BY name")
                            result = connection.execute(query,{"n":niche, "show": f"%{niche}%","username":session["username"]})
                            rows = result.fetchall()
                            if rows is None:
                                flash("No campaign found. Please check again.")
                                return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                            return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                    except Exception as e:
                        flash(f"Error occurred: {e}")
                        return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")

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
                                query = text("SELECT * FROM campaign WHERE visibility = :filterbyvalue AND started_by=:username ORDER BY name")
                                details = {"filterbyvalue" :filterbyvalue,"username":session["username"]}
                                result = connection.execute(query,details)
                                rows = result.fetchall()
                        
                                if rows is None:
                                    flash("No campaign found. Please check again.")
                                    return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                            
                                return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                            
                        elif filterbychoice =="isflagged":
                            if filterbyvalue == "not flagged":
                                filterbyvalue = 0
                            else:
                                filterbyvalue = 1
                            with db.engine.begin() as connection:
                                query = text("SELECT * FROM campaign WHERE isflagged = :filterbyvalue AND started_by=:username ORDER BY name")
                                details = {"filterbyvalue" :filterbyvalue,"username":session["username"]}
                                result = connection.execute(query,details)
                                rows = result.fetchall()
                        
                                if rows is None:
                                    flash("No campaign found. Please check again.")
                                    return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                            
                                return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")
                            
                        elif filterbychoice =="status":
                            date=datetime.now()
                            if filterbyvalue == "on going":
                                query = text(f"SELECT * FROM campaign WHERE end_date > '{date}' AND started_by = '{session["username"]}' AND start_date < '{date}' ORDER BY name")
                            
                            elif filterbyvalue == "scheduled":
                                query = text(f"SELECT * FROM campaign WHERE start_date > '{date}' AND started_by = '{session["username"]}' ORDER BY name")
                            
                            else:
                                query = text(f"SELECT * FROM campaign WHERE end_date < '{date}' AND started_by = '{session["username"]}' ORDER BY name")
                            with db.engine.begin() as connection:
                                
                                result = connection.execute(query)
                                rows = result.fetchall()
                        
                                if rows is None:
                                    flash("No campaign found. Please check again.")
                                    return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                            
                                return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")


                        else:
                            with db.engine.begin() as connection:
                                query = text("SELECT * FROM campaign WHERE category = :filterbyvalue AND started_by=:username ORDER BY name")
                                details = {"filterbyvalue" :filterbyvalue ,"username":session["username"]}
                                result = connection.execute(query,details)
                                rows = result.fetchall()
                        
                                if rows is None:
                                    flash("No user found. Please check again.")
                                    return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")
                            
                                return render_template("sponsor/myCampaigns.html",campaigns=rows,username=session["username"],new=row[0],method="GET")

                    except Exception as e:
                        flash(f"Error occurred: {e}")
                        return render_template("sponsor/myCampaigns.html",campaigns=campaigns,username=session["username"],new=row[0],method="GET")


@app.route("/sponsor/my_adRequests",methods=["GET","POST"])
@login_required
def sponsorAdRequests():

    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :username")
        details = {"username":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' ")
        details = {"username":session["username"]}
        results = connection.execute(query,details)
        ads = results.fetchall()


    if request.method == "POST":
        try:
            start = request.form["start"]
            end = request.form["end"]

            with db.engine.begin() as connection:
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.payment_amount >{int(start)} AND ad.payment_amount< {int(end)} ")
                details = {"username":session["username"]}
                results = connection.execute(query,details)
                a = results.fetchall()

            return render_template("sponsor/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")

        except:

            filterbychoice = request.form["filterbychoice"]
            filterbyvalue = request.form["filterbyvalue"]

            if filterbychoice=="category":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.category = '{filterbyvalue}' ")

            elif filterbychoice == "visibility":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.visibility = '{filterbyvalue}' ")

            elif filterbychoice == "status":
                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.status = '{filterbyvalue}' ")
            
            elif filterbychoice == "deleted":
                if filterbyvalue == "deleted":
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.deleted = 1 ")
                else:
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND ad.deleted = 0 ")


            else:
                if filterbyvalue == "flagged":
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.isflagged = 1 ")
                else:
                    query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND campaign.started_by = '{session["username"]}' AND campaign.isflagged = 0 ")

            with db.engine.begin() as connection:
                result = connection.execute(query)
                a = result.fetchall()

            return render_template("sponsor/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")


    return render_template("sponsor/adRequests.html",username=session["username"],new=row[0],ads=ads)


@app.route("/sponsor/delete_ad/<int:id>",methods=["GET"])
@login_required
def deleteSponsorAd(id):
    with db.engine.begin() as connection:
        query = text(f"UPDATE ad SET deleted = 1 WHERE id = {id}")
        connection.execute(query)
    return redirect(url_for("sponsorAdRequests"))

@app.route("/sponsor/accept/<int:id>")
def acceptAdS(id):

    with db.engine.begin() as connection:

        query = text(f"SELECT influencer FROM ad WHERE id = {id}")
        influencer = connection.execute(query).fetchone()[0]

        query = text(f"SELECT amount FROM negotiate WHERE message_id = {id} AND sent_to=:username ORDER BY id DESC LIMIT 1")
        amount = connection.execute(query,{"username":session["username"]}).fetchone()[0]

        query = text(f"UPDATE ad SET status = 'accepted',payment_amount= {amount} WHERE id = {id}")   
        connection.execute(query)

        query = text(f"UPDATE negotiate SET type= 'accepted' WHERE message_id ={id} AND type= 'negotiate' ")
        connection.execute(query)

    n = Message("Ad request negotiation accepted by sponsorer!",f"Ad request negotiation has been accepted.",session["username"],influencer,datetime.now(),"accepted",id)
    db.session.add(n)
    db.session.commit()

    flash("Ad request accepted.")
    return redirect(url_for("sponsorMessages"))

@app.route("/sponsor/edit_campaign/<int:id>",methods=["GET","POST"])
@login_required
def editCampaignDetails(id):

    indus=["Aerospace","Automotive","Education","Energy","Entertainment","Finance","Healthcare","Hospitality","Retail","Technology","Telecommunications"]
    category = ["Arts and Entertainment","Business","Designer","Education","Fashion and Beauty","Finance","Health and Wellness","Public Figure","Technology","Travel"]
    
    with db.engine.begin() as connection:
        query = text("SELECT newMessages FROM user WHERE username = :username")
        result = connection.execute(query,{"username":session["username"]})
        row = result.fetchone()

    with db.engine.begin() as connection:
        query = text("SELECT * FROM campaign WHERE id = :id AND started_by=:username")
        result = connection.execute(query,{"id":id,"username":session["username"]})
        rows = result.fetchone()

        if rows is None:
            return redirect(url_for("sponsorCampaigns"))

    if request.method=="POST":
        name = request.form["name"]
        description = request.form["description"]
        budget = request.form["budget"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        visibility = request.form["visibility"]
        goals = request.form["goals"]
        category = request.form["category"]
        niche = request.form["niche"]
        industry = request.form["industry"]

        

        date = start_date.split("-")
        start = datetime(int(date[0]),int(date[1]),int(date[2]))

        date = end_date.split("-")
        end = datetime(int(date[0]),int(date[1]),int(date[2]))

        with db.engine.begin() as connection:
            query = text(f"UPDATE campaign SET name='{name}',description='{description}',budget={int(budget)}, start_date='{start}',end_date='{end}',visibility='{visibility}',goals='{goals}',category='{category}',niche='{niche}',industry='{industry}' WHERE id={int(id)}")
            connection.execute(query)
            flash("Campaign details edited successfully!")
            return redirect(url_for("sponsorCampaigns"))

    return render_template("/sponsor/editCampaign.html",username=session["username"],new=row[0],userDetails=rows,industry=indus,category=category)


@app.route("/sponsor/accept_ad/<int:id>")
@login_required
def acceptAdApp(id):
    with db.engine.begin() as connection:
        query = text(f"UPDATE application SET type = 'accepted' WHERE message_id = {id}")
        connection.execute(query)

        query = text(f"SELECT sent_by,amount FROM application WHERE id = {id}")
        data = connection.execute(query).fetchone()
        

    box = AdRequest("Ad application","Ad application was taken.",id,data[0],session["username"],"accepted",data[1])
    db.session.add(box)
    db.session.commit()


    mess = Message("New Ad request!","New Ad request in the inbox!",session["username"],data[0],datetime.now(),"ad",-1)
    db.session.add(mess)
    db.session.commit()

    flash("Ad request accepted!")
    return redirect(url_for("sponsorMessages"))
    

@app.route("/sponsor/markAllRead")
def markAllReadS():
    with db.engine.begin() as connection:
        query = text(f"UPDATE message SET read = 1 WHERE sent_to = '{session["username"]}' ")
        connection.execute(query)

    return redirect(url_for("sponsorMessages"))


@app.route("/sponsor/markAllUnread")
def markAllUnreadS():
    with db.engine.begin() as connection:
        query = text(f"UPDATE message SET read = 0 WHERE sent_to = '{session["username"]}' ")
        connection.execute(query)

    return redirect(url_for("sponsorMessages"))


@app.route("/sponsor/reject_ad/<int:id>")
@login_required
def rejectAdApp(id):
    with db.engine.begin() as connection:
        query = text(f"UPDATE application SET type = 'rejected' WHERE message_id = {id}")
        connection.execute(query)

        query = text(f"SELECT sent_by FROM application WHERE message_id = {id}")
        data = connection.execute(query).fetchone()


    mess = Message("Ad application rejected!","Your ad request was rejected by the sponsorer!",session["username"],data[0],datetime.now(),"sent",-1)
    db.session.add(mess)
    db.session.commit()

    flash("Ad request rejected!")
    return redirect(url_for("sponsorMessages"))

@app.route('/sponsor/messages',methods=["GET","POST"])
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

        query = text("SELECT * FROM negotiate WHERE sent_to = :username AND type='negotiate' ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        ads = results.fetchall()

        query = text("SELECT * FROM application WHERE sent_to = :username AND type='application' ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        appli = results.fetchall()

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


    if request.method=="POST":
        try:
            id = request.form["ad_id"]
            amount = request.form["amount"]

            with db.engine.begin() as connection:
                query = text(f"SELECT influencer FROM ad WHERE id = {id}")
                influencer = connection.execute(query).fetchone()[0]
                

            n = Negotiate("Negotiation for ad request",f"Negotiation for ad request for an amount of ${amount}",session["username"],influencer,datetime.now(),"negotiate",id,amount)
            db.session.add(n)
            db.session.commit()

            flash("Negotiation request sent!")
            return render_template("sponsor/messages.html",ads=ads,all=all,read=read,unread=unread,username = session["username"],sent=sent,method="GET")
    
        except:
            id = request.form["a_id"]
            amount = request.form["amountN"]

            with db.engine.begin() as connection:
                query = text(f"SELECT sent_by FROM application WHERE message_id = {id}")
                influencer = connection.execute(query).fetchone()[0]

            n = Application("Negotiation for ad request",f"Negotiation for ad request for an amount of ${amount}",session["username"],influencer,datetime.now(),"application",id,amount)
            db.session.add(n)
            db.session.commit()

            flash("Negotiation request sent!")
            return render_template("sponsor/messages.html",ads=ads,all=all,read=read,unread=unread,username = session["username"],sent=sent,method="GET")
            
    return render_template("sponsor/messages.html",ads=ads,all=all,appli=appli,read=read,unread=unread,username = session["username"],sent=sent)
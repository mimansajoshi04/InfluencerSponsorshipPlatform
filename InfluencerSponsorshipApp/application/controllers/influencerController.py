from application.database import db,app
from flask import render_template,request,session,flash,redirect,url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from datetime import datetime
from application.models.messages import *
from application.models.user import *
from application.models.adRequest import *

def registerComplain(complain):
    
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
        
            query = text("UPDATE user SET newMessages = 1 WHERE username = :username")
            details = {"username":adminUsername}
            connection.execute(query,details)

    flash("Complain has been sent!")

    return

def findflagged():

    with db.engine.begin() as connection:
        query = text("SELECT isflagged FROM user WHERE username = :username")
        details = {"username":session["username"]}

        results = connection.execute(query,details)
        row = results.fetchone()

    return row[0]

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
    
@app.route('/influencer/messages',methods=["GET","POST"])
@login_required
def influencerMessages():

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

        query = text("SELECT * FROM negotiate WHERE sent_to = :username AND type = 'negotiate' ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        ads = results.fetchall()

        query = text("SELECT * FROM application WHERE sent_to = :username AND type = 'application' ORDER BY id DESC")
        details = {"username":session["username"]}
        results = connection.execute(query,details)

        appli = results.fetchall()

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
    
    if request.method == "POST":
        try:
            complain = request.form["complain_for_flag"]
            registerComplain(complain)

        except KeyError:
            try:
                amount = request.form["amount"]
                ad_id = request.form["ad_id"]

                with db.engine.begin() as connection:
                    query = text(f"SELECT sponsor FROM ad WHERE id = {ad_id}")
                    sponsor = connection.execute(query).fetchone()[0]
                

                n = Negotiate("Negotiation for ad request",f"Negotiation for ad request for an amount of ${amount}",session["username"],sponsor,datetime.now(),"negotiate",ad_id,amount)
                db.session.add(n)
                db.session.commit()

                flash("Negotiation request sent!")

            except KeyError:
                id = request.form["a_id"]
                amount = request.form["amountN"]

                with db.engine.begin() as connection:
                    query = text(f"SELECT sent_to FROM application WHERE message_id = {id}")
                    sponsor = connection.execute(query).fetchone()[0]

                n = Application("Negotiation for ad request",f"Negotiation for ad request for an amount of ${amount}",session["username"],sponsor,datetime.now(),"application",id,amount)
                db.session.add(n)
                db.session.commit()

                flash("Negotiation request sent!")

        finally:
            return render_template("influencer/messages.html",all=all,read=read,unread=unread,sent = sent,ads = ads,username = session["username"],flagged=findflagged(),method="GET")

    return render_template("influencer/messages.html",all=all,appli=appli,read=read,unread=unread,sent = sent,ads = ads,username = session["username"],flagged=findflagged())

@app.route("/influencer/mark_as_read/<id>")
def markAsReadI(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 1 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("influencerMessages"))

@app.route("/influencer/mark_as_unread/<id>")
def markAsUnreadI(id):
    with db.engine.begin() as connection:
        query = text("UPDATE message SET read = 0 WHERE id = :id")
        details = {"id":id}
        connection.execute(query,details)

    return redirect(url_for("influencerMessages"))

@app.route("/influencer/send_message",methods=["GET","POST"])
@login_required
def sendIMessage():

    if request.method =="POST":
            
        try : 
            complain = request.form["complain_for_flag"]
            registerComplain(complain)

            return render_template("/influencer/send_message.html",username=session["username"],flagged=findflagged(),method="GET")

        except KeyError:
        

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
            return redirect(url_for("influencerMessages"))

    return render_template("/influencer/send_message.html",username=session["username"],flagged=findflagged())

@app.route("/influencer/reply/<int:id>/<reciever>",methods=["GET","POST"])
@login_required
def influencerreply(id,reciever):

    
    if request.method=="POST":
            
        try:   
            complain = request.form["complain_for_flag"]
            registerComplain(complain)

            return render_template("influencer/reply_message.html",username=session["username"],flagged=findflagged(),method="GET")

        except KeyError:
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
            return redirect(url_for("influencerMessages"))
    else:
        return render_template("influencer/reply_message.html",username=session["username"],flagged=findflagged())
    

@app.route("/influencer/delete_account")
def deleteInfluencerAccount():

    username = session["username"]
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    user = Influencer.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    
    flash(f"User {username} has been permanantly deleted.")
    logout_user()

    return redirect(url_for("login"))

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

        query=text("SELECT newMessages FROM user WHERE username = :username")
        results=connection.execute(query,{"username":session["username"]})
        row=results.fetchone()


    if request.method == "POST":
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
    
    return render_template("influencer/dashboard.html",username=session["username"],new = row[0],flagged=findflagged())

@app.route("/influencer/settings",methods=["GET","POST"])
@login_required
def influencerSettings():

    categorys = ["Arts and Entertainment","Business","Designer","Education","Fashion and Beauty","Finance","Health and Wellness","Public Figure","Technology","Travel"]

    with db.engine.begin() as connection:
        query = text(f"SELECT influencer.name,user.username,user.email,influencer.category,influencer.niche,influencer.instaid,influencer.followers FROM user JOIN influencer ON user.username = influencer.username WHERE user.username = '{session["username"]}'")

        results = connection.execute(query)

        userDetails = results.fetchall()

        query = text("SELECT newMessages FROM user WHERE username = :user")
        details = {"user":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        if userDetails is None:
            flash("No user found!")
            return redirect(url_for("influencerDashboard"))
        

    if request.method == "POST":
            
        try:
            complain = request.form["complain_for_flag"]
            registerComplain(complain)
            return render_template("influencer/settings.html",userDetails = userDetails[0],new = row[0],username = session["username"],category=categorys,flagged=findflagged(),method="GET")

        except KeyError:

            name = request.form["name"]
            username = request.form["username"]
            email = request.form["email"]
            category = request.form["category"]
            niche = request.form["niche"]
            followers = request.form["followers"]
            insta_id = request.form["insta_id"]


            with db.engine.begin() as connection:

                orignalUN = session["username"]
                
                if username != orignalUN:
                    query = text("SELECT username FROM user WHERE username = :username")
                    details = {"username":username}

                    results = connection.execute(query,details)
                

                    if results.fetchall() != []:
                        flash("Username already exists. Try another username.")
                        return redirect(url_for("influencerSettings"))
                
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
                        return redirect(url_for("influencerSettings"))


                query = text("UPDATE user SET username = :username, email = :email WHERE username = :user")
                details = {"username":username,"email":email,"user" :session["username"]}

                connection.execute(query,details)

                query = text("UPDATE influencer SET username = :username, email = :email, name = :name,category= :category,niche=:niche,instaid=:insta_id,followers=:followers WHERE username = :user")
                details = {"name":name,"username":username,"email":email,"user" :session["username"],"category":category,"niche":niche,"followers":followers,"insta_id":insta_id}

                connection.execute(query,details)

                flash("User details edited!")

                query = text(f"SELECT influencer.name,user.username,user.email,influencer.category,influencer.niche,influencer.instaid,influencer.followers FROM user JOIN influencer ON user.username = influencer.username WHERE user.username = '{session["username"]}'")

                results = connection.execute(query)

                userDetails = results.fetchone()

                session["username"] = username

                query = text("SELECT newMessages FROM user WHERE username = :user")
                details = {"user":session["username"]}
                results = connection.execute(query,details)
                row = results.fetchone()


                return render_template("influencer/settings.html",username=session["username"],userDetails = userDetails,new = row[0],category=categorys,flagged=findflagged(),method="GET")
        

    return render_template("influencer/settings.html",userDetails = userDetails[0],new = row[0],username = session["username"],category=categorys,flagged=findflagged())

@app.route("/influencer/ad_requests",methods=["GET","POST"])
def influencerAd():

    with db.engine.begin() as connection:

        query = text("SELECT newMessages FROM user WHERE username = :user")
        details = {"user":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        query = text("SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND ad.influencer = :user")
        ads = connection.execute(query,details).fetchall()


    if request.method=="POST":
        try:
            complain = request.form["complain_for_flag"]
            registerComplain(complain)
            return render_template("influencer/adRequests.html",new=row[0],flagged=findflagged(),username=session["username"],ads=ads,method="GET")

        except KeyError:
                try:
                    id = request.form["ad_id"]
                    amount = request.form["amount"]

                    with db.engine.begin() as connection:
                        query = text(f"SELECT sponsor FROM ad WHERE id = {id}")
                        sponsor = connection.execute(query).fetchone()[0]

                    n = Negotiate("Negotiation for ad request",f"Negotiation for ad request for an amount of ${amount}",session["username"],sponsor,datetime.now(),"negotiate",id,amount)
                    db.session.add(n)
                    db.session.commit()

                    flash("Negotiation request sent!")
                    return render_template("influencer/adRequests.html",new=row[0],flagged=findflagged(),username=session["username"],ads=ads,method="GET")

                except KeyError:
                    try:
                        start = request.form["start"]
                        end = request.form["end"]

                        with db.engine.begin() as connection:
                            query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND ad.payment_amount >{int(start)} AND ad.payment_amount< {int(end)} AND ad.influencer = :username ")
                            details = {"username":session["username"]}
                            results = connection.execute(query,details)
                            a = results.fetchall()

                        return render_template("influencer/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")

                    except:

                        filterbychoice = request.form["filterbychoice"]
                        filterbyvalue = request.form["filterbyvalue"]

                        if filterbychoice=="category":
                            query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.category = '{filterbyvalue}' AND ad.influencer = :username ")

                        elif filterbychoice == "visibility":
                            query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.visibility = '{filterbyvalue}' AND ad.influencer = :username ")

                        elif filterbychoice == "status":
                            query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id AND ad.status = '{filterbyvalue}' AND ad.influencer = :username ")
                        
                        elif filterbychoice == "deleted":
                            if filterbyvalue == "deleted":
                                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND ad.deleted = 1 AND ad.influencer = :username ")
                            else:
                                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND ad.deleted = 0 AND ad.influencer = :username")


                        else:
                            if filterbyvalue == "flagged":
                                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.isflagged = 1 AND ad.influencer = :username")
                            else:
                                query = text(f"SELECT * FROM ad,campaign WHERE ad.campaign_id = campaign.id  AND campaign.isflagged = 0 AND ad.influencer = :username")

                        with db.engine.begin() as connection:
                            result = connection.execute(query,{"username":session["username"]})
                            a = result.fetchall()

                        return render_template("influencer/adRequests.html",username=session["username"],new=row[0],ads=a,method="GET")

    return render_template("influencer/adRequests.html",new=row[0],flagged=findflagged(),ads=ads,username=session["username"])

@app.route("/influencer/accept/<int:id>")
def acceptAd(id):

    with db.engine.begin() as connection:
        query = text(f"UPDATE ad SET status = 'accepted' WHERE id = {id}")   
        connection.execute(query)

        query = text(f"SELECT sponsor FROM ad WHERE id = {id}")
        sponsor = connection.execute(query).fetchone()[0]

        query = text(f"SELECT amount FROM negotiate WHERE message_id = {id} AND sent_to= :username ORDER BY id DESC LIMIT 1")
        amount = connection.execute(query,{"username":session["username"]}).fetchone()[0]

        query = text(f"UPDATE negotiate SET type='accepted',amount={amount} WHERE message_id={id}")
        connection.execute(query)

        query = text(f"UPDATE ad SET status='accepted',payment_amount={amount} WHERE id={id}")
        connection.execute(query)

    n = Message("Ad request accepted by influencer!",f"Ad request for your campaign has been accepted.",session["username"],sponsor,datetime.now(),"accepted",id)
    db.session.add(n)
    db.session.commit()

    flash("Ad request accepted.")
    return redirect(url_for("influencerAd"))

@app.route("/influencer/reject/<int:id>")
def rejectAd(id):

    with db.engine.begin() as connection:
        query = text(f"UPDATE ad SET status = 'rejected' WHERE id = {id}")   
        connection.execute(query)

        query = text(f"SELECT sponsor FROM ad WHERE id = {id}")
        sponsor = connection.execute(query).fetchone()[0]

        query = text(f"UPDATE negotiate SET type='rejected' WHERE message_id={id}")
        connection.execute(query)

    n = Message("Ad request rejected by influencer!",f"Ad request for your campaign has been rejected.",session["username"],sponsor,datetime.now(),"rejected",id)
    db.session.add(n)
    db.session.commit()

    flash("Ad request rejected.")
    return redirect(url_for("influencerAd"))


@app.route("/influencer/accept_ad/<int:c_id>/<int:id>")
def acceptNApp(id,c_id):
    with db.engine.begin() as connection:
        query = text(f"UPDATE application SET type = 'accepted' WHERE message_id = {id}")
        connection.execute(query)

        query = text(f"SELECT sent_by,amount FROM application WHERE id = {id}")
        data = connection.execute(query).fetchone()
        

    box = AdRequest("Ad application","Ad application was taken.",c_id,session["username"],data[0],"accepted",data[1])
    db.session.add(box)
    db.session.commit()


    mess = Message("New Ad request!","New Ad request in the inbox!",data[0],session["username"],datetime.now(),"ad",-1)
    db.session.add(mess)
    db.session.commit()

    flash("Ad request accepted!")
    return redirect(url_for("influencerMessages"))


@app.route("/influencer/markAllRead")
def markAllReadI():
    with db.engine.begin() as connection:
        query = text(f"UPDATE message SET read = 1 WHERE sent_to = '{session["username"]}' ")
        connection.execute(query)

    return redirect(url_for("influencerMessages"))


@app.route("/influencer/markAllUnread")
def markAllUnreadI():
    with db.engine.begin() as connection:
        query = text(f"UPDATE message SET read = 0 WHERE sent_to = '{session["username"]}' ")
        connection.execute(query)

    return redirect(url_for("influencerMessages"))

@app.route("/influencer/campaigns",methods=["GET","POST"])
@login_required
def seeCampaignsI():

    with db.engine.begin() as connection:

        query = text("SELECT newMessages FROM user WHERE username = :user")
        details = {"user":session["username"]}
        results = connection.execute(query,details)
        row = results.fetchone()

        query = text("SELECT * FROM campaign WHERE visibility = 'public' AND deleted = 0 ORDER BY name")
        results = connection.execute(query)
        all = results.fetchall()


    if request.method =="POST":
            
        try :

            complain = request.form["complainss"]
            campaign = int(request.form["complain_user"])

            with db.engine.begin() as connection:

                query=text("UPDATE campaign SET reports = reports + 1 WHERE id= :username")
                result = connection.execute(query,{"username":campaign})

                query=text("SELECT reports FROM campaign WHERE id= :username")
                result = connection.execute(query,{"username":campaign})
                rows = result.fetchone()

                if rows[0]>3:
                    query=text("UPDATE campaign SET isflagged = 1 WHERE id= :username")
                    connection.execute(query,{"username":campaign})

            new = Report(complain,session["username"],campaign,datetime.now(),'campaign')
            db.session.add(new)
            db.session.commit()

            return render_template("influencer/campaigns.html",username=session["username"],new=row[0],campaigns = all,flagged=findflagged(),method="GET")

        except KeyError:
            
            try:
                id = request.form["c_id"]
                amount = int(request.form["amount"])

                with db.engine.begin() as connection:
                    query = text(f"SELECT started_by FROM campaign WHERE id= {id}")
                    sponsor = connection.execute(query).fetchone()[0]

                mess = Application("New Ad request application!","New Ad request application in the inbox!",session["username"],sponsor,datetime.now(),"application",id,amount)
                db.session.add(mess)
                db.session.commit()

                mess = Message("New Ad request application!","New Ad request application in the inbox!",session["username"],sponsor,datetime.now(),"sent",-1)
                db.session.add(mess)
                db.session.commit()

                flash("Application for the Ad request is sent!")
                return redirect(url_for("influencerAd"))

                
            except KeyError:
                try:
                    complain = request.form["complain_for_flag"]
                    registerComplain(complain)
                    return render_template("influencer/campaigns.html",username=session["username"],new=row[0],campaigns = all,flagged=findflagged(),method="GET")
                

                except KeyError:
                
                    try:
                        name = request.form["name"]

                        try:
                            with db.engine.begin() as connection:
                                query = text("SELECT * FROM campaign WHERE (name = :name OR name LIKE :show) AND visibility = 'public' AND deleted = 0 ORDER BY name")
                                result = connection.execute(query,{"name":name, "show": f"%{name}%"})
                                rows = result.fetchall()
                                if rows is None:
                                    flash("No campaign found. Please check again.")
                                    return render_template("influencer/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                                return render_template("influencer/campaigns.html",campaigns=rows,username=session["username"],new=row[0],flagged=findflagged(),method="GET")
                        except Exception as e:
                            flash(f"Error occurred: {e}")
                            return render_template("influencer/campigns.html",campaigns=all,username=session["username"],new=row[0],flagged=findflagged(),method="GET")
                    
                    except KeyError:
                        try:
                            niche = request.form["n"]
                            try:
                                with db.engine.begin() as connection:
                                    query = text(f"SELECT * FROM campaign WHERE (niche = :n OR niche LIKE :show) AND visibility = 'public' AND deleted = 0 ORDER BY name")
                                    result = connection.execute(query,{"n":niche, "show": f"%{niche}%"})
                                    rows = result.fetchall()
                                    if rows is None:
                                        flash("No campaign found. Please check again.")
                                        return render_template("influencer/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                                    return render_template("influencer/campaigns.html",campaigns=rows,username=session["username"],new=row[0],flagged=findflagged(),method="GET")
                            except Exception as e:
                                flash(f"Error occurred: {e}")
                                return render_template("influencer/campaigns.html",campaigns=all,username=session["username"],new=row[0],flagged=findflagged(),method="GET")
                            
                        except KeyError:
                            filterbychoice = request.form["filterbychoice"]
                            filterbyvalue = request.form["filterbyvalue"] 

                            try:
                                if filterbychoice =="isflagged":
                                    if filterbyvalue == "not flagged":
                                        filterbyvalue = 0
                                    else:
                                        filterbyvalue = 1
                                    with db.engine.begin() as connection:
                                        query = text("SELECT * FROM campaign WHERE isflagged = :filterbyvalue AND visibility = 'public' AND deleted = 0 ORDER BY name")
                                        details = {"filterbyvalue" :filterbyvalue}
                                        result = connection.execute(query,details)
                                        rows = result.fetchall()
                                
                                        if rows is None:
                                            flash("No campaign found. Please check again.")
                                            return render_template("influencer/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                                    
                                        return render_template("influencer/campaigns.html",campaigns=rows,username=session["username"],new=row[0],flagged=findflagged(),method="GET")
                                    
                                elif filterbychoice =="status":
                                    date=datetime.now()
                                    if filterbyvalue == "on going":
                                        query = text(f"SELECT * FROM campaign WHERE end_date > '{date}' AND start_date < '{date}' AND visibility = 'public' AND deleted = 0  ORDER BY name")
                                    
                                    elif filterbyvalue == "scheduled":
                                        query = text(f"SELECT * FROM campaign WHERE start_date > '{date}' AND visibility = 'public' AND deleted = 0 ORDER BY name")
                                    
                                    else:
                                        query = text(f"SELECT * FROM campaign WHERE end_date < '{date}' AND visibility = 'public' AND deleted = 0 ORDER BY name")
                                    with db.engine.begin() as connection:
                                        
                                        result = connection.execute(query)
                                        rows = result.fetchall()
                                
                                        if rows is None:
                                            flash("No campaign found. Please check again.")
                                            return render_template("influencer/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                                    
                                        return render_template("influencer/campaigns.html",campaigns=rows,username=session["username"],new=row[0],flagged=findflagged(),method="GET")


                                else:
                                    with db.engine.begin() as connection:
                                        query = text("SELECT * FROM campaign WHERE category = :filterbyvalue AND visibility = 'public' AND deleted = 0 ORDER BY name")
                                        details = {"filterbyvalue" :filterbyvalue}
                                        result = connection.execute(query,details)
                                        rows = result.fetchall()
                                
                                        if rows is None:
                                            flash("No user found. Please check again.")
                                            return render_template("influencer/campaigns.html",campaigns=all,username=session["username"],new=row[0],method="GET")
                                    
                                        return render_template("influencer/campaigns.html",campaigns=rows,username=session["username"],new=row[0],flagged=findflagged(),method="GET")

                            except Exception as e:
                                flash(f"Error occurred: {e}")
                                return render_template("influencer/campaigns.html",campaigns=all,username=session["username"],new=row[0],flagged=findflagged(),method="GET")




    return render_template("influencer/campaigns.html",username=session["username"],new=row[0],campaigns = all,flagged=findflagged())
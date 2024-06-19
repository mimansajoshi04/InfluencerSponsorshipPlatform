from application.database import db,app
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from flask import url_for


from application.models.user import *
from application.models.messages import *
from application.models.campaign import *
from application.models.adRequest import *


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='/login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


from application.controllers.auth import *
from application.controllers.sponsorController import *
from application.controllers.influencerController import *
from application.controllers.adminController import *





if __name__=="__main__":
    with app.app_context():
       db.create_all()
    app.run(debug=True,host='0.0.0.0',port=8080,threaded=True)

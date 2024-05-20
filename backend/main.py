from flask import Flask, render_template
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.data.database import db
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.data.models import User, Role, Sponsor, Influencer, Campaign, AdRequest
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from create_roles import create_roles
from flask_security import utils
from dotenv import load_dotenv
load_dotenv()

app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    app.app_context().push()
    db.init_app(app)
    app.app_context().push()

    # Setup Flask Security
    # user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    # security = Security(app, user_datastore)
    api = Api(app)
    app.app_context().push()
    
    db.create_all()

    if not Role.query.all():
        create_roles()

    return app, api

app, api = create_app()
jwt = JWTManager(app)
# Import all the controllers so they are loaded
from application.controller.controllers import *

# Importing all APIs
from application.controller.api import SignupAPI,LoginAPI,ProfileAPI
api.add_resource(SignupAPI, "/api/signup")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(ProfileAPI, "/api/profile")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080,debug=True)

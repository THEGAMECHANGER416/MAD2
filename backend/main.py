from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from application import config
from application.config import LocalDevelopmentConfig, StageConfig
from application.data.database import db
from application import worker
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.data.models import User, Role, Sponsor, Influencer, Campaign, AdRequest
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from create_roles import create_roles
from flask_security import utils
from dotenv import load_dotenv
from flask_mail import Mail, Message
from celery.schedules import crontab
import os
from flask_sse import sse
load_dotenv()

app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        app.logger.info("Production config has not been implemented yet")
        raise Exception("Production config has not been implemented yet")
    if os.getenv('ENV', "development") == "stage":
        app.config.from_object(StageConfig)
    else:
        app.config.from_object(LocalDevelopmentConfig)
    app.app_context().push()
    db.init_app(app)
    app.app_context().push()

    api = Api(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})
    app.app_context().push()

    # Create celery instance
    celery = worker.celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        broker_connection_retry_on_startup=True,
        timezone='Asia/Kolkata',
    )
    celery.Task = worker.ContextTask
    db.create_all()

    if not Role.query.all():
        create_roles()

    return app, api, celery

app, api, celery = create_app()
app.register_blueprint(sse, url_prefix='/stream')
mail = Mail(app)
jwt = JWTManager(app)

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory('application/uploads', filename)

# Import all the controllers so they are loaded
from application.controller.controllers import *

# Importing all APIs
from application.controller.api import SignupAPI, LoginAPI, ProfileAPI, CampaignAPI, AdRequestAPI, SearchAPI
api.add_resource(SignupAPI, "/api/signup")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(ProfileAPI, "/api/profile")
api.add_resource(CampaignAPI, '/api/campaigns', '/api/campaigns/<int:campaign_id>')
api.add_resource(AdRequestAPI, '/api/ad_requests', '/api/ad_requests/<int:ad_request_id>')
api.add_resource(SearchAPI, '/api/search')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

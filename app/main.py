import os
from flask import Flask,request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_bootstrap import Bootstrap
from datetime import timedelta
from .views import views
from .database import create_db
from .config_other import init
from werkzeug.utils import secure_filename
def add_views(app):
    for view in views:
        app.register_blueprint(view)

def loadConfig(app,config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    delta = 7
    if app.config['ENV'] == "DEVELOPMENT":
        print(app.config.from_pyfile('config.py'))
        app.config.from_pyfile('config.py')
        # delta = app.config['JWT_EXPIRATION_DELTA']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        # delta = os.environ.get('JWT_EXPIRATION_DELTA', 7)
        
    # app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=int(delta))
        
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__,static_url_path='/static')
    bootstrap = Bootstrap(app)
    CORS(app)
    loadConfig(app,config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEVER_NAME'] = '0.0.0.0'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    add_views(app)
    create_db(app)
    init(app)
    app.app_context().push()
    return app
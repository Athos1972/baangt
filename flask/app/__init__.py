import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


#
# configurations
#
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'secret!key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or \
    'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'testrun.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import views, models
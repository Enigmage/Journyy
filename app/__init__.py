from flask import Flask, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flaskext.markdown import Markdown
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate
from config import Config
from oauthlib.oauth2 import WebApplicationClient


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app) # Serializer
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)
moment = Moment(app)
md = Markdown(app)
client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

from app import routes, models



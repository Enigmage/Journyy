
from flask import Flask, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flaskext.markdown import Markdown
from flask_simplemde import SimpleMDE
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app) # Serializer
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)
moment = Moment(app)
mde = SimpleMDE(app)
md = Markdown(app)

from app import routes, models



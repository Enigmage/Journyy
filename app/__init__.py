from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flaskext.markdown import Markdown
from flask_simplemde import SimpleMDE


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app) # Serializer
mde = SimpleMDE(app)
md = Markdown(app)

from app import routes, models



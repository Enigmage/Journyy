import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID') or None
    GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET') or None
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
   # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')



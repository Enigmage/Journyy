from app import db, ma, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from time import time
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(200), unique = True)
    passwd = db.Column(db.String(200))
    posts = db.relationship('Content', backref='author', lazy='dynamic')

    def generate_reset_password_token(self, expires=900):
        return jwt.encode({'reset-pass': self.id, 'expiration-time':time()+expires}, 
                          app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms = ['HS256'])['reset-pass']
        except:
            return
        return User.query.get(id)

    def set_passwd(self, passwd):
        self.passwd =  generate_password_hash(passwd)
    
    def check_passwd(self, passwd):
        return check_password_hash(self.passwd,passwd)

    def __repr__(self):
        return f"Username:{self.username}"


@login_manager.user_loader 
def load(id):
    return User.query.get(int(id))

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    timestamp = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Content id {self.id}"




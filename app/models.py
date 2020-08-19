from app import db, ma
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(200), unique = True)
    passwd = db.Column(db.String(200))
    posts = db.relationship('Content', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"Username:{self.username}"


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    timestamp = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Content id {self.id}"

class ContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Content



from app import db, ma
from datetime import datetime

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"Content id {self.id}"

class ContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Content



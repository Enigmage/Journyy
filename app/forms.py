from flask_wtf import FlaskForm
from wtforms import SubmitField

class markdownform(FlaskForm):
    submit = SubmitField('Post')

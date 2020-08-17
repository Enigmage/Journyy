from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class markdownform(FlaskForm):
    submit = SubmitField('Post')

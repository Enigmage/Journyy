from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class markdownform(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=2, max=80)])
    pagedown = PageDownField('Post', validators=[DataRequired()])
    submit = SubmitField('Post')

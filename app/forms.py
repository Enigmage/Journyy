from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class markdownform(FlaskForm):
    submit = SubmitField('Post')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me Logged in')
    submit = SubmitField('Log In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already exists!!")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exists')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Enter registered email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Enter new password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')




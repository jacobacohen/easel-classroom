from flask_login import current_user
#from flask_user import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import SelectMultipleField, StringField, IntegerField, SubmitField, TextAreaField, PasswordField, RadioField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)


from ..models import User


# Registration Fields: Full Name, Email, Password, Student or Teacher selection
class RegistrationForm(FlaskForm):
    givenname = StringField('Given name', validators=[InputRequired(), Length(min=4, max=80)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    user_type = RadioField('Teacher or Student?', choices=[('Teacher', 'Teacher'), ('Student', 'Student')])
    password = PasswordField('Password (Requirements: 8 character minimum with 1 or more uppercase, lowercase, digit and special characters (!,@,#,$,%,^,&,*,(,)-,=,+))', validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')

    def validate_email(self, email):        
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is taken')

    def validate_password(self, password):
        pw = password.data
        special = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+']
        if not any(c.isupper() for c in pw):
            raise ValidationError('No uppercase characters detected')
        if not any(c.islower() for c in pw):
            raise ValidationError('No lowercase characters detected')
        if not any(c.isdigit() for c in pw):
            raise ValidationError('No digit characters detected')
        if not any(c in special for c in pw):
            raise ValidationError('No special characters detected')

class MessageComposeForm(FlaskForm):
    sending_to = SelectMultipleField("Select 1 or more recipients", validators=[InputRequired()])
    message_title = StringField("Message title (40 char or less)", validators=[InputRequired(), Length(min=1, max=40)])
    content = TextAreaField("Message body (1000 char or less)", validators=[InputRequired(), Length(min=1, max=1000)])

    submit = SubmitField('Send')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("Login")

class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("Change Username")

    def validate_username(self, username):
        existing_user = User.objects(username=username.data).first()
        if existing_user is not None:
            raise ValidationError('Username is taken')


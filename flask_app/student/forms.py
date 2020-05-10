from flask_wtf import FlaskForm
from flask_login import current_user
#from flask_user import current_user
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)


from ..models import User

class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField('Search')

class MovieReviewForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Enter Comment')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
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

# TODO
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

class UpdateProfilePicForm(FlaskForm):
    pass

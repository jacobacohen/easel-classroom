from flask_wtf import FlaskForm
from flask_login import current_user
#from flask_user import current_user
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)


from ..models import User

class ClassCreateForm(FlaskForm):
    class_id = StringField('Class ID (Max 8 characters, alphabet characters will convert to be capitalized, Required)', validators=[InputRequired(), Length(min=1, max=8)])
    class_name = StringField('Longer Classname (Required)', validators=[InputRequired(), Length(min=1, max=100)])
    class_size = IntegerField('Maximum Class Capacity (Not required, cap up to 1000 available)', validators=[NumberRange(min=0, max=1000)])
    description = TextAreaField('Description of Class (Not required)', validators=[Length(min=0, max=1000)])
    submit = SubmitField('Create Classroom')

class AssignmentCreateForm(FlaskForm):
    assignment_name = StringField('Name for assignment (20 character max)', validators=[InputRequired(), Length(min=1, max=20)])
    assignment_type = StringField('Assignment Type (20 character max)', validators=[InputRequired(), Length(min=1, max=20)])
    points = IntegerField('Points Assignment is worth', validators=[InputRequired()])
    description = TextAreaField('Assignment description (1000 character max, not required)', validators=[Length(min=0, max=1000)])

    submit = SubmitField('Create Classroom')



class GradingForm(FlaskForm):
    pass

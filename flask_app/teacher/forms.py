from flask_wtf import FlaskForm
from flask_login import current_user
#from flask_user import current_user
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)


from ..models import *

class ClassCreateForm(FlaskForm):
    class_id = StringField('Class ID (Max 8 characters, alphabet characters will convert to be capitalized, Required)', validators=[InputRequired(), Length(min=1, max=8)])
    class_name = StringField('Longer Classname (Required)', validators=[InputRequired(), Length(min=1, max=100)])
    class_size = IntegerField('Maximum Class Capacity (Not required, cap up to 1000 available)', validators=[NumberRange(min=0, max=1000)])
    description = TextAreaField('Description of Class (Not required)', validators=[Length(min=0, max=1000)])

    submit = SubmitField('Create Classroom')

class AssignmentCreateForm(FlaskForm):
    assignment_name = StringField('Name for assignment (20 character max, must be unique per class)', validators=[InputRequired(), Length(min=1, max=20)])
    assignment_type = StringField('Assignment Type (20 character max)', validators=[InputRequired(), Length(min=1, max=20)])
    points = IntegerField('Points Assignment is worth', validators=[InputRequired()])
    description = TextAreaField('Assignment description (1000 character max, not required)', validators=[Length(min=0, max=1000)])
    # hacky way to validate for assignment name by class_id

    submit = SubmitField('Create Classroom')

    def validate_assignment_name(self, assignment_name):
        class_id = AssignmentCreateForm.get_class_id()
        if Assignment.objects(parent_class=load_class(class_id), assignment_name=assignment_name.data).first() != None:
            raise ValidationError("Duplicate assignment name submitted")


class GradingForm(FlaskForm):
    assignment = SelectField('Assignment Select', validators=[InputRequired()])
    student = SelectField('Student Select', validators=[InputRequired()])
    grade = IntegerField('Points given for assignment', validators=[InputRequired(), NumberRange(min=0)])

    submit = SubmitField('Grade')

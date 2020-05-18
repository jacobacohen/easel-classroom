from flask_login import UserMixin
#from flask_user import UserManager, UserMixin
from datetime import datetime
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

def load_class(class_id):
    return Classroom.objects(class_id=class_id).first()

def load_assignment(assignment_name, class_id):
    return Assignment.objects(assignment_name=assignment_name, parent_class=class_id).first()

class User(db.Document, UserMixin):
    fullname = db.StringField(required=True)
    username = db.StringField(unique=True, required=True)
    email = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    user_type = db.StringField(required=True)
    classes = db.ListField(db.ReferenceField('Classroom'))
    #profile_pic = 
    #.modify method to change data

    # Returns unique string identifying our object
    def get_id(self):
        return self.username 

# Try to move this back to __init__
# Setup Flask-User and User data-model
# user_manager = UserManager(app, db, User)

# Overall classroom structure
class Classroom(db.Document):
    teacher = db.ReferenceField(User, required=True)
    class_id = db.StringField(unique=True, required=True, min_length=4, max_length=8)
    classname = db.StringField(required=True, min_length=1, max_length=100)
    description = db.StringField(max_length=1000)
    assignments = db.ListField(db.ReferenceField('Assignment'))
    students = db.ListField(db.ReferenceField('User'))
    class_size = db.IntField(min_value=0, max_value=1000)

    def get_id(self):
        return self.class_id

class Message(db.Document):
    sender = db.ReferenceField('User', required=True)
    reciever = db.ReferenceField('User', required=True)
    classroom = db.ReferenceField('Classroom', required=True)
    content = db.StringField(required=True, min_length=1, max_length=1000)
    unread = db.BooleanField(default=True)
    timestamp = db.DateTimeField(auto_now_add=True)

    def get_id(self):
        return str(self.timestamp) +  str(self.sender) + str(self.reciever)

class Assignment(db.Document):
    # TODO: must be unique within a class
    assignment_name = db.StringField(required=True, min_length=1, max_length=20)
    assignment_type = db.StringField(required=True, min_length=1, max_length=20)
    points = db.IntField(min_value=0)
    description = db.StringField(min_length=0, max_length=1000)
    parent_class = db.ReferenceField('Classroom', required=True)
    grades = db.ListField(db.ReferenceField('Grade'))

    def get_id(self):
        return str(self.name) + str(self.parent_class) + str(self.grades)

class Grade(db.Document):
    student = db.ReferenceField('User', required=True)
    parent_assignment = db.ReferenceField('Assignment', required=True)
    grade = db.IntField(required=True)

    def get_id(self):
        return str(self.student) +  str(self.parent_assignment) + str(self.grade)

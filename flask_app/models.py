from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager, utils

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    fullname = db.StringField(required=True)
    username = db.StringField(unique=True, required=True)
    email = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    user_type = db.StringField(required=True)
    classes = db.ListField()
    #profile_pic = 
    #.modify method to change data

    # Returns unique string identifying our object
    def get_id(self):
        return self.username 

# Overall classroom structure
class Classroom(db.Document):
    teacher = db.ReferenceField(User, required=True)
    classname = db.StringField(unique=True, required=True, min_length=4, max_length=8)
    classdescription = db.StringField()
    #assignments = db.
    #students = db.

class Message(db.Document):
    sender = db.ReferenceField(User, required=True)
    reciever = db.ReferenceField(User, required=True)
    classroom = db.ReferenceField(Classroom, required=True)
    content = db.StringField(required=True, min_length=1, max_length=600)

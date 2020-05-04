from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager, utils

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True)
    email = db.StringField(unique=True, required=True)
    password = db.StringField()
    #profile_pic = 
    #.modify method to change data

    # Returns unique string identifying our object
    def get_id(self):
        return self.username 

class Review(db.Document):
    # required reference to User
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(unique=True, required=True)
    date = db.StringField(required=True)
    imdb_id = db.StringField(required=True, min_length=9, max_length=9)
    movie_title = db.StringField()

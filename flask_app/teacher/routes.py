# 3rd-party packages
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
#from flask_user import current_user, UserManager, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from .. import app, bcrypt
from .forms import *
#from ..models import User, load_user
from ..models import *
from ..utils import role_required, current_time

teacher = Blueprint("teacher", __name__)

@teacher.route('/user/<username>')
def user_info(username):
    user = User.objects(username=username).first()

    # user exists
    #if user is not None:
    #    user_reviews = Review.objects(commenter=user)
    #    return render_template("user_detail.html", error=None, username=username, reviews=user_reviews, total_reviews=len(user_reviews))
        #return render_template("user_detail.html", error=None)
    # user does not exist
    #return render_template("user_detail.html", error="No such user", username=username, reviews=None, total_reviews=0)

""" ************ User Management views ************ """
@teacher.route('/account', methods=['GET', 'POST'])
@role_required(role='Teacher')
def account():
    # get all taught classes
    taught_classes = Classroom.objects(teacher=load_user(current_user.username))
    # TODO: Classroom creator/options, messages/inbox
    #if username_update.validate_on_submit():
        # perform username update
        #new_username = username_update.username.data
        #user = load_user(current_user.username), 
        #user = User.objects(username=current_user.username).first()

        # check uniqueness
        #user.modify(username=new_username)
        #user.save()
        #return render_template('teacher-account.html', username_form=username_update, picture_form=picture_update)
    
    #if picture_update.validate_on_submit():
    #    return render_template('teacher-account.html', username_form=username_update, picture_form=picture_update)

    return render_template('teacher-account.html', taught_classes=taught_classes, msg=None)

# page that loads the classroom creator
@teacher.route('/class-creation', methods=['GET', 'POST'])
@role_required(role='Teacher')
def class_creator():
    form = ClassCreateForm()

    if form.validate_on_submit():
        # instantiate class size if not given
        class_size = 0 if form.class_size == None else form.class_size.data
        new_class = Classroom(teacher=load_user(current_user.username), class_id=form.class_id.data, classname=form.class_name.data,
                class_size = class_size, description=form.description.data, students=[], assignments=[])
        new_class.save()
        return redirect(url_for('teacher.account', msg='Class successfully created'))
    return render_template('class-create.html', form=form)

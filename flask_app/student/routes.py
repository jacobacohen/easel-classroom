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
from ..models import User, Classroom, load_user
from ..utils import role_required, current_time

student = Blueprint("student", __name__)

@student.route('/user/<username>')
def user_detail(username):
    user = User.objects(username=username).first()

    return "filler"
    # user exists
    #if user is not None:
    #    user_reviews = Review.objects(commenter=user)
    #    return render_template("user_detail.html", error=None, username=username, reviews=user_reviews, total_reviews=len(user_reviews))
        #return render_template("user_detail.html", error=None)
    # user does not exist
    #return render_template("user_detail.html", error="No such user", username=username, reviews=None, total_reviews=0)

""" ************ User Management views ************ """

@student.route('/account', methods=['GET', 'POST'])
@role_required(role='Student')
def account():
    username_update = UpdateUsernameForm()
    picture_update = UpdateProfilePicForm()

    if username_update.validate_on_submit():
        # perform username update
        new_username = username_update.username.data
        user = load_user(current_user.username), 
        user = User.objects(username=current_user.username).first()

        # check uniqueness
        user.modify(username=new_username)
        user.save()
        return render_template('studnet-account.html', username_form=username_update, picture_form=picture_update)

    if picture_update.validate_on_submit():
        return render_template('student-account.html', username_form=username_update, picture_form=picture_update)

    return render_template('student-account.html', username_form=username_update, picture_form=picture_update)

@student.route('/class-join', methods=['GET', 'POST'])
@role_required(role='Student')
def class_join():
    # get list of classes to join (that student isn't already in)
    open_classes = []
    open_seats = "No Limit"
    for unenrolled in Classroom.objects(students__nin=[load_user(current_user.username)]):
        print(unenrolled.students)
        # check for open seats
        # no seating limit
        if unenrolled.class_size == None or unenrolled.class_size == 0:
            open_classes.append((unenrolled, open_seats))
        # seating limit check
        elif len(unenrolled.students) < unenrolled.class_size:
            open_seats = unenrolled.class_size - len(unenrolled.students)
            open_classes.append((unenrolled, open_seats))

    return render_template('class-join.html', form=None, open_classes=open_classes, open_seats=open_seats)

@student.route('/enroll/<class_id>', methods=['GET'])
@role_required(role='Student')
def enroll(class_id):
    # Add student to class' students and redirect to the course page
    class_adding = Classroom.objects(class_id=class_id).first()
    # double check class availability
    if not (class_adding.class_size == None or class_adding.class_size == 0) and len(class_adding.students) >= class_adding.class_size:
        return "Class full - could not enroll"
    # check if student already in class
    if load_user(current_user.username) in class_adding.students:
        return "Already enrolled"
    else:
        class_adding.update(students=class_adding.students.append(load_user(current_user.username)))
        class_adding.save()
        return redirect(url_for('main.course_page', class_id=class_id))

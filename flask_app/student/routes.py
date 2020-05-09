# 3rd-party packages
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from .. import app, bcrypt
from .forms import * 
from ..models import User, load_user
from ..utils import current_time

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
@login_required
def account():
    username_update = UpdateUsernameForm()
    picture_update = UpdateProfilePicForm()

    if username_update.validate_on_submit():
        # perform username update
        new_username = username_update.username.data
        #user = load_user(current_user.username), 
        user = User.objects(username=current_user.username).first()

        # check uniqueness
        user.modify(username=new_username)
        user.save()
        return render_template('account.html', username_form=username_update, picture_form=picture_update)

    if picture_update.validate_on_submit():
        return render_template('account.html', username_form=username_update, picture_form=picture_update)

    return render_template('account.html', username_form=username_update, picture_form=picture_update)

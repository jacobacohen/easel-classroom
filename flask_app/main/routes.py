# 3rd-party packages
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_mongoengine import MongoEngine
from flask_login import current_user, login_user, logout_user, login_required
#from flask_user import current_user, UserManager, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from .. import app, bcrypt
from .forms import *
from ..models import * 
from ..utils import *

# Main includes any pages viewable by new users, or that might be shared by teachers and students
main = Blueprint("main", __name__)
""" ************ View functions ************ """
@main.route('/', methods=['GET', 'POST'])
def index():
    # need to check user student or teacher to link correct account page
    #if current_user.is_authenticated:
    #    return render_template('index.html')
    return render_template('index.html')

""" ************ Account Creation/Login views ************ """
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    # successful add
    if form.validate_on_submit():
        hashedpwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(fullname=form.givenname.data, username=form.username.data, email=form.email.data,
                password=hashedpwd, user_type=form.user_type.data)
        new_user.save()
        return redirect(url_for('main.login'))

    return render_template("register.html", form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('account'))

    form = LoginForm()

    if form.validate_on_submit():
        user = load_user(form.username.data)

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.user_type == 'Student':
                return redirect(url_for('student.account'))
            if user.user_type == 'Teacher':
                return redirect(url_for('teacher.account'))

    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
""" ************ Teacher/Student Shared views ************ """
@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # TEACHER: get all taught classes
    if current_user.user_type == "Teacher":
        taught_classes = Classroom.objects(teacher=load_user(current_user.username))
        return render_template('teacher-account.html', taught_classes=taught_classes, msg=None)
    # STUDENT: get all enrolled classes
    else:
        enrolled_classes = Classroom.objects(students__in=[load_user(current_user.username)])
        return render_template('student-account.html', enrolled_classes=enrolled_classes, msg=None)


@main.route('/courses/<class_id>')
@login_required
def course_page(class_id):
    # not enrolled, redirect
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))
    return str(class_id)

""" ************ Account Creation/Login views ************ """
@main.route('/credits', methods=['GET'])
def credits():
    return render_template('credits.html')

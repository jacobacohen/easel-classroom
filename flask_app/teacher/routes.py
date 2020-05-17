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
from ..utils import role_required, current_time, enroll_required

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
    return render_template('teacher-account.html', taught_classes=taught_classes, msg=None)

# page that loads the classroom creator
@teacher.route('/class-creation', methods=['GET', 'POST'])
@role_required(role='Teacher')
def class_creator():
    form = ClassCreateForm()

    if form.validate_on_submit():
        # instantiate class size if not given
        class_size = 0 if form.class_size == None else form.class_size.data
        new_class = Classroom(teacher=load_user(current_user.username), class_id=form.class_id.data.upper(), classname=form.class_name.data,
                class_size = class_size, description=form.description.data, students=[], assignments=[])
        new_class.save()
        return redirect(url_for('main.course_page', class_id=form.class_id.data.upper(), msg='Class successfully created'))
    return render_template('class-create.html', form=form)


@teacher.route('/courses/<class_id>/students')
@role_required(role='Teacher')
def students(class_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))
    cls = Classroom.objects(class_id=class_id).first()
    studs = list(cls.students)
    assignments = list(cls.assignments)
    # TODO: Add student grades here 
    return render_template('class-students.html', students=studs, assignments=assignments)

@teacher.route('/courses/<class_id>/create-assignment', methods=['GET', 'POST'])
@role_required(role='Teacher')
def create_assignment(class_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))
    form = AssignmentCreateForm()

    if form.validate_on_submit():
        # add assignment to classroom in database
        new_assign = Assignment(assignment_name=form.assignment_name.data,
                assignment_type=form.assignment_type.data, points=form.points.data,
                grades=[], parent_class=load_class(class_id))
        new_assign.save()
        return redirect(url_for('teacher.grade_modify', class_id=class_id))

    return render_template('assign-create.html', form=form, class_id=class_id)


@teacher.route('/courses/<class_id>/grading')
@role_required(role='Teacher')
def grade_modify(class_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))

    form = AssignmentCreateForm()
    return render_template('grading.html', form=form, class_id=class_id)


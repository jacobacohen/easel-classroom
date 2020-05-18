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

""" ************ User Management views ************ """
@teacher.route('/account', methods=['GET', 'POST'])
@role_required(role='Teacher')
def account():
    # get all taught classes
    taught_classes = Classroom.objects(teacher=load_user(current_user.username))
    return render_template('teacher-account.html', taught_classes=taught_classes, msg=None)

""" ************ Teacher user views ************ """
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
    # Get dictionary with students and grade objects
    cls = Classroom.objects(class_id=class_id).first()
    studs = list(cls.students)
    student_class = {}
    for s in studs:
        student_class[s] = []
    assignments = list(Assignment.objects(parent_class=cls))
    for grade in Grade.objects(parent_assignment__in=assignments):
        if student_class.get(grade.student) == None:
            student_class[grade.student] = [(grade.parent_assignment.assignment_name, grade.grade)]
        else:
            student_class[grade.student].append((grade.parent_assignment.assignment_name, grade.grade))
    # TODO: Add student grades here 
    return render_template('class-students.html', students=studs, student_class=student_class)

@teacher.route('/courses/<class_id>/create-assignment', methods=['GET', 'POST'])
@role_required(role='Teacher')
def create_assignment(class_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))
    # Make it so we can get the class id
    setattr(AssignmentCreateForm, "get_class_id", lambda : class_id)
    # class_id passed in as prefix
    form = AssignmentCreateForm()

    if form.validate_on_submit():
        # add assignment to classroom in database
        new_assign = Assignment(assignment_name=form.assignment_name.data,
                assignment_type=form.assignment_type.data, points=form.points.data,
                grades=[], description=form.description.data, parent_class=load_class(class_id))
        new_assign.save()
        return redirect(url_for('teacher.grade_modify', class_id=class_id))

    return render_template('assign-create.html', form=form, class_id=class_id)


@teacher.route('/courses/<class_id>/grading', methods=['GET', 'POST'])
@role_required(role='Teacher')
def grade_modify(class_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))

    # Get students enrolled in class and assignments in class
    cls = Classroom.objects(class_id=class_id).first()
    students = []
    for s in cls.students:
        students.append((s.username, s.fullname + " (" + s.username + ")"))
    assignments = []
    for a in Assignment.objects(parent_class=load_class(class_id)):
        assignments.append((a.assignment_name, a.assignment_name + " (Worth " + str(a.points) + " Points)" ))

    # Get students enrolled in class and assignments in class
    form = GradingForm()
    form.student.choices=students
    form.assignment.choices = assignments
    if form.validate_on_submit():
        cls = load_class(class_id)
        a_modify = Assignment.objects(parent_class=cls, assignment_name=form.assignment.data).first()
        print(a_modify)
        #print(assignment_modify)
        # submit grade for student (or modify if existing
        previous_grade = Grade.objects(student=load_user(form.student.data), parent_assignment=a_modify).first()
        # modify
        if previous_grade != None:
            print("we do this?")
            previous_grade.update(grade=form.grade.data)
            previous_grade.save()
        # no need to update the assignments list as it's a reference
        # create new grade
        else:
            new_grade = Grade(student=load_user(form.student.data), parent_assignment=a_modify,
                grade=form.grade.data)
            new_grade.save()
            # need to update assignments list
            grades_list = list(a_modify.grades)
            a_modify.update(grades=grades_list.append(new_grade))
            a_modify.save()
        # redirect to the same grade submit page
        return redirect(url_for('teacher.grade_modify', class_id=class_id))
    return render_template('grading.html', form=form, class_id=class_id)


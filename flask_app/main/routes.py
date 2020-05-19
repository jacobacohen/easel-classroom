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
    # Get open classes for homepage
    open_classes = []
    for cls in Classroom.objects():
        if cls.class_size == None or len(cls.students) < cls.class_size or cls.class_size == 0:
            open_classes.append(cls)
    return render_template('index.html', open_classes=open_classes)

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
    # if teacher
    cur_class = Classroom.objects(class_id=class_id).first()
    unreads = len(Message.objects(recipients__in=[load_user(current_user.username)], classroom=load_class(class_id), unread=True))
    if current_user.user_type == "Teacher":
        # Featured content: Students enrolled, create assignment, assign grades, send message, inbox
        return render_template('teacher-class.html', cur_class=cur_class, teaching=len(cur_class.students), unreads=unreads)
    # if student
    if current_user.user_type == "Student":
        # Featured content: View assignments, grades, Send a message
        # Get assignment and grade if recieved
        assignments = []
        for a in Assignment.objects(parent_class=load_class(class_id)):
            if Grade.objects(student=load_user(current_user.username)) != None:
                assignments.append((a, "Grade recieved"))
            else:
                assignments.append((a, "Not yet graded"))
        return render_template('student-class.html', assignments=assignments, cur_class=cur_class, unreads=unreads)

@main.route('/courses/<class_id>/compose', methods=["GET", "POST"])
@login_required
def message(class_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))
    setattr(MessageComposeForm, "get_class_id", lambda : class_id)
    form = MessageComposeForm()

    # set recipient choices for form
    cur_class = load_class(class_id)
    user = load_user(current_user.username)
    could_recieve = []
    # add students
    for person in list(cur_class.students):
        if person != user:
            could_recieve.append((person.username, person.fullname + " (Student)"))
    # add teacher if not teacher
    if current_user.user_type == "Student":
        could_recieve.append((cur_class.teacher.username, cur_class.teacher.fullname + " (Teacher)"))
    form.sending_to.choices = could_recieve

    if form.validate_on_submit():
        #Create message with all the intended recipients
        recipients = []
        for u in form.sending_to.data:
            recipients.append(load_user(u))
        new_message = Message(sender=user, classroom=cur_class, content=form.content.data,
                message_title=form.message_title.data, recipients=recipients)
        new_message.save()
        return redirect(url_for('main.message', class_id=class_id))

    return render_template("compose.html", form=form, class_id=class_id)


@main.route('/courses/<class_id>/inbox')
@login_required
def inbox(class_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))
    # TODO: return list of recieved messages
    messages = list(Message.objects(classroom=load_class(class_id), recipients__in=[load_user(current_user.username)]))
    return render_template("inbox.html", messages=messages, class_id=class_id)

@main.route('/courses/<class_id>/inbox/<m_id>')
@login_required
def message_page(class_id, m_id):
    if not enroll_required(class_id):
        return redirect(url_for('main.index'))
    # mark as read
    m = Message.objects(id=m_id).first()
    m.modify(unread=False)
    m.save()
    return render_template("message-page.html", m=m, class_id=class_id)

""" ************ Account Creation/Login views ************ """
@main.route('/credits', methods=['GET'])
def credits():
    return render_template('credits.html')

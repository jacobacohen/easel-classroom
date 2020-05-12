from datetime import datetime
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user, login_manager
from .models import load_user, Classroom 

def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

# login_required wrapper to extend roles to flask-login
# See https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes
def role_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
            # Msg? Just go to index?
                return redirect(url_for('main.index'))
            if ((current_user.user_type != role) and (role != "ANY")):
                return redirect(url_for('main.index'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# enrolled in class or teaching class required to view course page
def enroll_required(class_id):
    # login_required catches is_authenticated
    # Class must exist
    if len(Classroom.objects(class_id=class_id)) == 0:
        return False
    # Teacher must be teaching the class
    if (current_user.user_type == 'Teacher') and (len(Classroom.objects(teacher=load_user(current_user.username))) == 0):
        return False
    # Student must be enrolled in the class
    if (current_user.user_type == 'Student') and (len(Classroom.objects(students__in=[load_user(current_user.username)])) == 0):
        return False
    return True

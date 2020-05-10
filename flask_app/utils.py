from datetime import datetime
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user, login_manager

def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

# login_required wrapper to extend roles to flask-login
# See https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes
def role_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            print(dir(login_manager))
            if not current_user.is_authenticated:
            # Msg? Just go to index?
                return redirect(url_for('main.index'))
            if ((current_user.user_type != role) and (role != "ANY")):
                return redirect(url_for('main.index'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

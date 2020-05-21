# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
#flask_user will allow role management
#from flask_user import current_user, UserManager, login_required
from flask_talisman import Talisman
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime

app = Flask(__name__)
#content security policy
csp = {
    'default-src': [
        '\'self\'',
        '*.bootstrapcdn.com',
        '*.jquery.com',
        '*.jsdelivr.net'
        ]
        }
Talisman(app, content_security_policy=csp)
# check before committing
# app.config["MONGO_URI"] = "mongodb://localhost:27017/second_database"
#app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/easel'
#real mongodb_host
app.config['MONGODB_HOST'] = 'mongodb://heroku_jfhgfss2:4veq0p63f9hsj089qu8iree88t@ds139884.mlab.com:39884/heroku_jfhgfss2?retryWrites=false'

app.config['SECRET_KEY'] = os.environ.get('EASEL_SECRET')

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
bcrypt = Bcrypt(app)

# blueprints
from flask_app.main.routes import main
from flask_app.teacher.routes import teacher 
from flask_app.student.routes import student

app.register_blueprint(main)
app.register_blueprint(teacher)
app.register_blueprint(student)

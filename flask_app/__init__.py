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
# app.config["MONGO_URI"] = "mongodb://localhost:27017/second_database"
#app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/easel'
#real mongodb_host
app.config['MONGODB_HOST'] = 'mongodb://heroku_jfhgfss2:4veq0p63f9hsj089qu8iree88t@ds139884.mlab.com:39884/heroku_jfhgfss2'
# TODO: Use os.envrion secret key
app.config['SECRET_KEY'] = '\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'

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

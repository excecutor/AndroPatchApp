#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask import session, g
from flask.ext.login import login_user , logout_user , current_user , login_required
from flask.ext.login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import string
from flask import send_from_directory
from werkzeug import secure_filename
import os
import logging
import re
import ast






app = Flask(__name__)

loglevel = logging.DEBUG 
logging.basicConfig(filename='/tmp/example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')

ALLOWED_EXTENSIONS = set(['apk', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.secret_key = 'never know key?'
app.config['DATABASE_FILE'] = '/tmp/mysql_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['UPLOAD_FOLDER'] = '../upload/'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'upload'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create user model.
class User(db.Model):
           id = db.Column(db.Integer, primary_key=True)
           username = db.Column(db.String(100))
           last_name = db.Column(db.String(100)) 
           login = db.Column(db.String(80), unique=True)
           email = db.Column(db.String(120))
           password = db.Column(db.String(64))
         

# Flask-Login integration
           def check_password(self , password):
                  user = self.get_user()
                  return  check_password_hash(user.password , password)
           def get_user(self):
               return db.session.query(User).filter_by(login=self.login).first()
           def is_authenticated(self):
               return True
           def is_active(self):
               return True
           def is_anonymous(self):
               return False
           def get_id(self):
               return self.id
# Required for administrative interface
           def __unicode__(self):
               return self.username

def build_sample_db():

          import string
          import random
          db.drop_all()
          db.create_all()
# passwords are hashed, to use plaintext passwords instead:
          test_user_1 = User(login="t3Us3r", password=generate_password_hash("p@ssw0rd*"),last_name='lastTest')
          db.session.add(test_user_1)
          test_user_2 = User(login="mspn", password=generate_password_hash("@ndr0P@tch@pp"),last_name='lastTest')
          db.session.add(test_user_2)
          test_user_3 = User(login="operando", password=generate_password_hash("op3rand0!op3rand0!"),last_name='lastTest')
          db.session.add(test_user_3)

          db.session.commit()
          return


###############################################
build_sample_db()






@app.route('/login',methods=['GET','POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True


    registered_user = db.session.query(User).filter_by(login=username).first()

 
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid','error')
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)

    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('upload'))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and 'somefile' in request.files:
        file = request.files['somefile']
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filename)
            filename
            print 'Filename Upload:' , filename
            adnet  =  request.form['adnet']
            method =  request.form['method']
            adnet = adnet.strip(' ')
            method = method.strip(' ')


            pipe = subprocess.Popen("python ../start.py  "  + filename + "  --extract=decompile  --mode=" + method + " --netad=" + adnet, stdout=subprocess.PIPE, stderr=None, shell=True)
            result = pipe.stdout.read()

            final = string.split(result, '\n')  # --> ['Line 1', 'Line 2', 'Line 3']

            d_filename = 'sign.patched.' + filename[10:]
            flash('Signed Apk started to download.Look your browser download folder')
            return send_from_directory(app.config['UPLOAD_FOLDER'],d_filename, as_attachment=True)
        else: flash ('Wrong FileType') 

    return render_template('upload.html')


@app.route('/')
def home():
   return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port = 2123)

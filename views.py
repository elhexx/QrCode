from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField
from passlib.hash import sha256_crypt
import gc
from functools import wraps

'''
from createData import createData
from flask_mysqldb import  MySQL
from MySQLdb import escape_string as thwart
from database import Database
from functools import wraps
'''
from main import app
from models import createUser, getUsers, update_user, delete_user, get_admin, create_admin
from forms import RegistrationForm


@app.route('/')
def index():
    return render_template('index.html')

"""--------Security-----------"""
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


"""-----ADDING DATA---------"""
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        ch = 0
        msg = "User added successfully"
        try:
            createUser(fname, lname)
            jsonObject = getUsers()
            return render_template('add.html', msg=msg, data=jsonObject)
        except Exception as e:
            return e.message
    if request.method == 'GET':
        jsonObject = getUsers()
        #return jsonObject
        return render_template('add.html', data = jsonObject)
"""-----UPDATING DATA---------"""
@app.route("/upd", methods=['GET','POST'])
def upd():
    fname = request.form['fname']
    lname = request.form['lname']
    try:
        update_user(fname, lname)
        return "Done"
    except Exception as e:
        return e.message

#"""----- DELETE DATA---------"""
@app.route("/del", methods=['GET','POST'])
def Del():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        try:
            delete_user(fname, lname)
            jsonObject = getUsers()
            return render_template('del.html', data=jsonObject)
        except Exception as e:
            return e.message
    if request.method == 'GET':
        jsonObject = getUsers()
        return render_template('del.html', data=jsonObject)

@app.route("/dashboard")
def get():
    jsonObject = getUsers()

    #return jsonObject
    return render_template('dashboard.html', data=jsonObject)
    #return render_template('test.html', data=jsonObject)


"""-------------Login Page---------------------"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = str(request.form['password'])
        user = get_admin(username)
        if user:
            if sha256_crypt.verify(password, str(user.password)):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else :
                return render_template('login.html', msg="incorrect password")
        else :
            return render_template('login.html', msg="user not found")


    if request.method == 'GET':
        return render_template('login.html')

"""************REGISTER*****************************"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        username = form.username.data
        password = sha256_crypt.encrypt((str(form.password.data)))
        create_admin(username, password)
        return "success"
        #else :
         #   return render_template('register.html', msg= form.errors, form = form)

"""******************LOG OUT****************"""
@is_logged_in
@app.route('/logout')
def logout():
    session.clear()
    flash('you are logged out', 'success')
    return redirect(url_for('login'))
from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify, g
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField
from passlib.hash import sha256_crypt
import gc
from functools import wraps
from functools import wraps

from main import app
from models import createUser, getUsers, update_user, delete_user, get_admin, create_admin, reset_user, generate_qr
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
@is_logged_in
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
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        if fname and lname:
            try:
	            msg = update_user(fname, lname)
	            return msg
            except Exception as e:
                return e.message
        else:
            return "not valid"
    if request.method == 'GET':
        jsonObject = getUsers()
        return render_template('upd.html', data=jsonObject)



@app.route("/reset", methods=['GET','POST'])
@is_logged_in
def reset():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        try:
            reset_user(fname, lname)
            jsonObject = getUsers()
            return render_template('reset.html', data=jsonObject)
        except Exception as e:
            return e.message
    if request.method == 'GET':
        jsonObject = getUsers()
        return render_template('reset.html', data=jsonObject)


#"""----- DELETE DATA---------"""
@app.route("/del", methods=['GET','POST'])
@is_logged_in
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


@app.route('/generate', methods=['GET','POST'])
@is_logged_in
def generate():
	if request.method == 'GET':
		return render_template('generate.html', src='')
	elif request.method == 'POST':
		fname = request.form['fname']
    	lname = request.form['lname']
    	if fname and lname:
			generate_qr(fname, lname)
			return render_template('generate.html', src = fname+'.png')
	return render_template('generate.html', src='')



@app.route("/dashboard")
@is_logged_in
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
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('you are logged out', 'success')
    return redirect(url_for('login'))



@app.route("/chart")
def chart():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [100,90,80,70,60,40,70,80]
    return render_template('chart.html', values=values, labels=labels)

from main import db
import pyqrcode
from datetime import datetime

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    CH = db.Column(db.Integer, default = 0)
    time = db.Column(db.DateTime)


    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
        self.time = ''

    def __repr__(self):
        return '<User %r>' % self.id

"""ADMIN INFO"""
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

"""ADMIN FUNCTIONS"""
def get_admin(username):
    admin = Admin.query.filter_by(username=username).first()
    return admin


def create_admin(username, password):
    db.create_all()
    admin = Admin(username, password)
    db.session.add(admin)
    db.session.commit()

"""USER FUNCTIONS"""
def createUser(fname, lname):
    db.create_all()
    user = Students(fname, lname)
    db.session.add(user)
    db.session.commit()

def getUsers():
    users = Students.query.all()
    return users

def update_user(fname, lname):
    db.create_all()
    user = Students.query.filter_by(fname = fname, lname = lname).first()
    if user:
        if user.CH:
            return "already exist"
        user.CH = 1
        user.time = str(datetime.utcnow()).split('.')[0]
        db.session.add(user)
        db.session.commit()
        return "done"
    return "user does not exist"

def reset_user(fname, lname):
    db.create_all()
    user = Students.query.filter_by(fname = fname, lname = lname).first()
    user.CH = 0
    user.time = ''
    db.session.add(user)
    db.session.commit()

def delete_user(fname, lname):
    db.create_all()
    user = Students.query.filter_by(fname=fname, lname=lname).first()
    db.session.delete(user)
    db.session.commit()


def generate_qr(fname, lname): 
    qr = pyqrcode.create(fname+' '+lname)
    qr.png('static/img/'+fname+'.png', scale=7)
    
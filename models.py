from main import db

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    CH = db.Column(db.Integer, default = 0)

    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

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
    user = Students.query.filter_by(fname = fname, lname = lname).first()
    user.CH = 1
    db.session.add(user)
    db.session.commit()

def delete_user(fname, lname):
    user = Students.query.filter_by(fname=fname, lname=lname).first()
    db.session.delete(user)
    db.session.commit()
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms import validators
from wtforms.validators import InputRequired


class RegistrationForm(Form):
    fname = StringField('First Name', [validators.Length(min=4, max=20)])
    lname = StringField('Last Name', [validators.Length(min=4, max=20)])
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email', [validators.Length(min=4, max=20)])
    password = PasswordField('New Password', [
        validators.data_required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')



class AddNewProductForm(Form):
    name = StringField('name', [InputRequired()])
    price = StringField('price', [InputRequired()])
    stock = StringField('stock', [InputRequired ()])
    description = TextAreaField('description', [InputRequired()])
    category = StringField('category', [InputRequired()])
    pictures = StringField('pictures', [InputRequired()])
    specifications = StringField('specifications', [InputRequired(message="Completeaza ba specificatiile")])
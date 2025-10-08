from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    
    email = StringField('Email Address')
    password = StringField('Password' )    
    submit = SubmitField("Submit")
    SignIn = SubmitField("Sign In")

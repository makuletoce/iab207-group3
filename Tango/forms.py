from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[validators.email()])
    password = StringField('Password', validators=[validators.data_required()])    
    submit = SubmitField("Submit")
    SignIn = SubmitField("Sign In")

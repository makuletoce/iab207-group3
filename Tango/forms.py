from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    
    email = StringField('Email Address', validators=[DataRequired()])
    password = StringField('Password' , validators=[DataRequired()])    
    submit = SubmitField("Submit")
    SignIn = SubmitField("Sign In")


class SignUpForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = StringField('Password' , validators=[DataRequired()])    
    address = StringField('Street Address', validators=[DataRequired()])

    submit = SubmitField("Submit")
    SignUp = SubmitField("Sign In")

class EventManagement(FlaskForm):
    
    event_name = StringField('Event Name')
    event_date = StringField('Event Date')
    event_time = StringField('Event Time')
    location = StringField('Location')
    my_dropdown = SelectField('Choose an Option', choices=[
            ('option1_value', 'Option 1 Display'),
            ('option2_value', 'Option 2 Display'),
            ('option3_value', 'Option 3 Display')], validators=[DataRequired()])

    description = StringField('Description')

    submit = SubmitField("Submit")


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, PasswordField, TelField, TimeField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required")
        ])
    submit = SubmitField("Submit")


class SignUpForm(FlaskForm):
    
    first_name = StringField(
        'First Name',
        validators=[DataRequired(message="First name is required")]
    )
    last_name = StringField(
        'Last Name',
        validators=[DataRequired(message="Last name is required")]
    )
    phone = TelField(
        'Phone Number',
        validators=[DataRequired(message="Phone number is required")]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Password is required")]
    )
    address = StringField(
        'Street Address',
        validators=[DataRequired(message="Address is required")]
    )
    submit = SubmitField("Submit")

class EventManagement(FlaskForm):
    
    event_name = StringField('Event Name')
    event_date = DateField('Event Date')
    event_time = TimeField('Event Time')
    location = StringField('Location')
    num_of_tickets = IntegerField("Spaces Available")
    catagory = SelectField('Catagory', choices=[
            ('Casual', 'Casual'),
            ('Competative', 'Competative'),
            ('Social', 'Social')], validators=[DataRequired()])

    description = StringField('Description')

    submit = SubmitField("Submit")

class TicketForm(FlaskForm):
    
    quantity = IntegerField("Ticket Amount", validators=[DataRequired()])
    submit = SubmitField("Attend")


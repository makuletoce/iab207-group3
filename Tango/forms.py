from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    
    email = StringField('Email Address', validators=[DataRequired()])
    password = StringField('Password' , validators=[DataRequired()])    
    submit = SubmitField("Submit")


class SignUpForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = StringField('Password' , validators=[DataRequired()])    
    address = StringField('Street Address', validators=[DataRequired()])

    submit = SubmitField("Submit")

class EventManagement(FlaskForm):
    
    event_name = StringField('Event Name')
    event_date = StringField('Event Date')
    event_time = StringField('Event Time')
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

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit_comment = SubmitField('Post')


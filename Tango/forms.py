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
    
    title = StringField('Event Name')
    date = StringField('Event Date')
    time = StringField('Event Time')
    location = StringField('Location')
    availability = IntegerField("Spaces Available")
    catagory = SelectField('Catagory', choices=[
            ('Casual', 'Casual'),
            ('Competative', 'Competative'),
            ('Social', 'Social')], validators=[DataRequired()])

    description = StringField('Description')

    submit = SubmitField("Submit")

    cancel = SubmitField('cancel')

class TicketForm(FlaskForm):
    
    quantity = IntegerField("Ticket Amount", validators=[DataRequired()])
    submit = SubmitField("Attend")

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit_comment = SubmitField('Post')


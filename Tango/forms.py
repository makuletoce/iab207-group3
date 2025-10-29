from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField,
    IntegerField, DateField, TimeField, TelField
)
from wtforms.validators import DataRequired, NumberRange, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=8, max=15)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    address = StringField('Street Address', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Submit")



class EventManagement(FlaskForm):
    
    title = StringField('Event Name', validators=[DataRequired(), Length(max=100)])
    date = StringField('Event Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = StringField('Event Time', format='%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    availability = IntegerField("Spaces Available", validators=[DataRequired(), NumberRange(min=1)])
    catagory = SelectField('Catagory', choices=[
            ('Casual', 'Casual'),
            ('Competative', 'Competative'),
            ('Social', 'Social')], validators=[DataRequired()])

    description = StringField('Description',  validators=[DataRequired(), Length(max=500)])
    image = FileField('Event Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

    submit = SubmitField("Submit")

    cancel = SubmitField('cancel')

class TicketForm(FlaskForm):
    
    quantity = IntegerField("Ticket Amount", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Attend")

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit_comment = SubmitField('Post')


from flask import Blueprint, render_template, request, session, redirect, url_for
from .forms import EventManagement, TicketForm
from .models import Ticket, Event
from flask_login import login_required, current_user

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def landing():
    events = Event.query.all()
    return render_template('index.html', events=events)

@mainbp.route('/managment')
@login_required
def eventManagment():
    Event_Management_form = EventManagement()
    if Event_Management_form.validate_on_submit():
        return render_template('/')

    return render_template('event_managment.html', form=Event_Management_form)

@mainbp.route('/history')
@login_required
def eventHistory():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    for ticket in tickets:
        print(ticket)
    return render_template('booking_history.html', tickets=tickets)

@mainbp.route('/details/<int:event_id>')
def eventDetails(event_id):
    event = Event.query.get_or_404(event_id)
    form = TicketForm()
    return render_template('event_details.html', event=event)

# @mainbp.route('/login')
# def login():
#     login_form = LoginForm()
#     if login_form.validate_on_submit():
#         return redirect('/')
#     return render_template('Login.html', form=login_form)

# @mainbp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     SignUp_form = SignUpForm()
#     if SignUp_form.validate_on_submit():
#         print("Form has been Validated")

#         new_user = User(first_name=SignUp_form.first_name.data, 
#                         last_name=SignUp_form.last_name.data,
#                         phone_number=SignUp_form.phone.data, 
#                         email=SignUp_form.email.data, 
#                         password_hash=SignUp_form.password.data,
#                         address=SignUp_form.address.data)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect('/')

#     return render_template('SignUp.html', form=SignUp_form)


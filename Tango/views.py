from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .forms import EventManagement, TicketForm
from .models import Ticket, Event, Comment
from flask_login import login_required, current_user
from . import db
from datetime import date, datetime
from sqlalchemy.orm import joinedload

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def landing():
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('index.html', events=events)

@mainbp.route('/managment', methods=['GET', 'POST'])
@login_required
def eventManagment():
    form = EventManagement()

    today = date.today().isoformat()  # e.g. "2025-10-29"

    if form.validate_on_submit():

        # --- Duplicate title check ---
        existing_event = Event.query.filter_by(title=form.event_name.data).first()
        if existing_event:
            flash("An event with this title already exists. Please choose another title.", "danger")
            return render_template('event_managment.html', form=form, today=today)

        # --- If no duplicate, proceed ---
        event_date = form.event_date.data  # datetime.date

        new_event = Event(
            title=form.event_name.data,
            description=form.description.data,
            image='casual-image.jpg',
            availability=form.num_of_tickets.data,
            status='Available',
            date=event_date,
            time=form.event_time.data, 
            category=form.category.data,
            location=form.location.data,
            host=current_user.id
        )

        db.session.add(new_event)
        db.session.commit()
        print("Event saved to database!")

        return redirect(url_for("main.landing"))
    
    else:
        print("Form did NOT validate")
        print(form.errors)

    return render_template('event_managment.html', form=form, today=today)
    

@mainbp.route('/history')
@login_required
def eventHistory():
    # pass all tickets of the logged in user to the page
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('booking_history.html', tickets=tickets)

@mainbp.route('/details/<int:event_id>', methods=['GET', 'POST'] )
def eventDetails(event_id):

    # get event id from url
    event = Event.query.get_or_404(event_id)
    form = TicketForm()
    error = None

    # --- Update event status BEFORE display (for GET requests too) ---
    if event.availability == 0:
        event.status = 'Sold Out'
    elif event.availability <= 15:
        event.status = 'Low Availability'
    else:
        event.status = 'Available'
    db.session.commit()

    

    # pull comments for this event and eager-load each comment's user
    comments = (
        Comment.query
        .options(joinedload(Comment.user))        # so c.user is usable in the template
        .filter_by(event_id=event.id)
        .order_by(Comment.date_posted.desc())
        .all()
    )

        
    if form.validate_on_submit():
         
        # if not logged in
        if  not current_user.is_authenticated:
            error="You need to be logged in to attend events"
            flash(error)
            return redirect(url_for("auth.login"))
        
        elif event.availability < form.quantity.data:
            error="There are not enough tickets to complete Purchase"

        
        
        # make a new ticket for the amount of tickets ordered
        else:
            event.availability = event.availability - form.quantity.data

            
            for new_ticket in range(form.quantity.data):
                new_ticket = Ticket(purchase_date = date.today(),
                                    event_id = event.id,
                                    user_id = current_user.id)
                db.session.add(new_ticket)


             #-------- Update event status again after purchase-------
            if event.availability == 0:
                event.status = 'Sold Out'
            elif event.availability <= 15:
                event.status = 'Low Availability'
            else:
                event.status = 'Available'


            db.session.commit()
            flash("Tickets successfully purchased!")
            return redirect(url_for("main.landing"))
            
    return render_template('event_details.html', event=event, form=form, comments=comments, error=error)

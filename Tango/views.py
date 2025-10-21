from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .forms import EventManagement, TicketForm
from .models import Ticket, Event, Comment
from flask_login import login_required, current_user
from . import db
from datetime import date
from sqlalchemy.orm import joinedload

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def landing():
    events = Event.query.all()
    return render_template('index.html', events=events)

@mainbp.route('/managment', methods=['GET', 'POST'] )
@login_required
def eventManagment():
    form = EventManagement()
    if form.validate_on_submit():
        new_event = Event(title = form.event_name.data,
                          description = form.description.data,
                          date = form.event_date.data,
                          time = form.event_time.data,
                          location = form.location.data,
                          catagory = form.catagory.data,
                          availability = form.num_of_tickets.data,
                          host = current_user.id
                          )
        
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("main.landing"))

    return render_template('event_managment.html', form=form)

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

# ------------- TICKET STATUS SECTION ------------- #


    # ----- Check ticket availability -----
    if event.availability <= 0:
        event.status = 'Sold Out'
        db.session.commit()
        flash("Tickets are sold out for this event!", "danger")
        return redirect(url_for('main.events'))

    # ----- Simulate a ticket purchase -----
    event.availability -= 1

    # ----- Update status dynamically -----
    if event.availability == 0:
        event.status = 'Sold Out'
    elif event.availability < 10:  # optional threshold
        event.status = 'Low Availability'
    else:
        event.status = 'Available'

    db.session.commit()
    flash(f"Ticket purchased! {event.availability} remaining.", "success")

    # ------------- COMMENTS SECTION ------------- 

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
            db.session.commit()
            return redirect(url_for("main.landing"))
            
    return render_template('event_details.html', event=event, form=form, comments=comments, error=error)


# create_db.py
from datetime import datetime, timedelta
from Tango import create_app, db
from Tango.models import Event  # important: import models so SQLAlchemy knows them

app = create_app()

with app.app_context():
    db.create_all()  # creates events, users, tickets, comments tables

    # Seed one event if none exist
    if not Event.query.first():
        e = Event(
            title="CS:GO open",
            description="Demo seeded event",
            image="/static/img/competative-image.jpg",
            availability=100,
            start_date=datetime.now() + timedelta(days=7),
            end_date=datetime.now() + timedelta(days=7, hours=2),
        )
        db.session.add(e)
        db.session.commit()

print("Database initialized and (optionally) seeded.")

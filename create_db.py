# create_db.py
from Tango import create_app, db     # your factory and SQLAlchemy instance
# If models aren't imported in __init__, import them here to register
from Tango import models             # ensures models metadata is known to SQLAlchemy

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created in Tango.db")

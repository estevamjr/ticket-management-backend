import os
from app.models.user import User
from app.extensions import db

DB_PATH = 'database.db'

def resetAndCreateDb(app, create_default_user=True):
    with app.app_context():
        db.create_all()
        if create_default_user:
            pass
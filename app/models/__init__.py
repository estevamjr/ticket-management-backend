from flask import Flask
from app.extensions import db

from .user import User
from .attachment import Attachment
from .ticket import Ticket
from .log import Log

def create_database(app: Flask):
    with app.app_context():
        db.create_all()
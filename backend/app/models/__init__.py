from flask import Flask
from app.extensions import db

def create_database(app: Flask):
    with app.app_context():
        db.create_all()
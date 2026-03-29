from app.extensions import db, bcrypt
import uuid
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()
        )
    )
    username = db.Column(
        db.String(80), 
        unique=True, 
        nullable=False
    )
    
    password_hash = db.Column(
        db.String(128), 
        nullable=True
    )
    
    tickets_created = db.relationship(
        'Ticket', 
        foreign_keys='Ticket.user_id', 
        back_populates='creator', 
        lazy='dynamic'
    )
    tickets_assigned = db.relationship(
        'Ticket', 
        foreign_keys='Ticket.assignee_id', 
        back_populates='assignee', 
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(
            self.password_hash, 
            password
        )

    def to_json(self):
        return {
            "id": self.id, 
            "username": self.username
        }
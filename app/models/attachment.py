from app.extensions import db
import uuid
from datetime import datetime

class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()
                        )
    )
    file_url = db.Column(
        db.String(255), 
        nullable=False
    )
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow
    )
    
    user_id = db.Column(
        db.String(36), 
        db.ForeignKey('users.id'), 
        nullable=False
    )
    ticket_id = db.Column(
        db.String(36), 
        db.ForeignKey('tickets.id'), 
        nullable=False
    )
    
    uploader = db.relationship(
        'User', 
        backref='attachments'
    )
    ticket = db.relationship(
        'Ticket', 
        back_populates='attachments'
    )

    def to_json(self):
        return {
            "id": self.id, 
            "file_url": self.file_url, 
            "user_id": self.user_id
        }
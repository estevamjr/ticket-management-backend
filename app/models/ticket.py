from app.extensions import db
import uuid
from datetime import datetime
from flask import Flask

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # Corrigido: default=lambda:
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open', nullable=False)
    priority = db.Column(db.String(20), default='high', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    comments = db.Column(db.String(300), default='...', nullable=True)
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False) # Criador
    assignee_id = db.Column(db.String(36), db.ForeignKey('users.id')) # Atribuído
    
    attachments = db.relationship('Attachment', back_populates='ticket', lazy=True)
    
    creator = db.relationship('User', foreign_keys=[user_id], back_populates='tickets_created')
    assignee = db.relationship('User', foreign_keys=[assignee_id], back_populates='tickets_assigned')

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'priority': self.priority,
            'assignee_id': self.assignee_id,
            'comments': self.comments,
            'attachments': [attachment.to_json() for attachment in self.attachments] if self.attachments else []
        }
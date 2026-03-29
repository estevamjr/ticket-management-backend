from app.extensions import db
import uuid
from datetime import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    timestamp = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )
    
    action = db.Column(
        db.String(100), 
        nullable=False
    )
    
    details = db.Column(
        db.String(255), 
        nullable=True
    )

    cpu_usage = db.Column(
        db.Float, 
        nullable=True
    )
    
    ram_usage = db.Column(
        db.Float, 
        nullable=True
    )
    
    active_threats = db.Column(
        db.Integer, 
        nullable=True
    )
    
    untrusted_processes = db.Column(
        db.Integer, 
        nullable=True
    )
    
    andon_status = db.Column(
        db.Integer, 
        nullable=True
    ) # 0, 1 ou 2
    
    user_id = db.Column(
        db.String(36), 
        db.ForeignKey('users.id'), 
        nullable=True
    )
    
    user = db.relationship(
        'User', 
        backref=db.backref('logs', lazy=True)
    )

    def to_json(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "details": self.details,
            "user_id": self.user_id,
            "cpu_usage": self.cpu_usage,
            "ram_usage": self.ram_usage,
            "active_threats": self.active_threats,
            "untrusted_processes": self.untrusted_processes,
            "andon_status": self.andon_status
        }
#
# COPIE E COLE ISSO EM: app/models/log.py
#
from app.extensions import db
import uuid
from datetime import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(255), nullable=True)
    
    # ESTE É O CAMPO QUE O ERRO DIZ QUE NÃO EXISTE
    # Vamos garantir que ele exista e seja salvo.
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Relacionamento (Opcional, mas bom ter)
    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def to_json(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "details": self.details,
            "user_id": self.user_id
        }
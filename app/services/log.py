#
# COPIE E COLE ISSO EM: app/services/log.py
#
from app.extensions import db
from app.models.log import Log
from sqlalchemy import desc

class LogService:
    
    @staticmethod
    def getAll() -> list[Log]:
        try:
            return Log.query.order_by(db.desc(Log.timestamp)).all()
        except Exception as e:
            print(f"Error getting all logs: {e}")
            raise e

    @staticmethod
    def create_log(action: str, details: str, user_id: str = None): # Aceita user_id
        """
        Cria um novo registro de log.
        """
        try:
            new_log = Log(
                action=action, 
                details=details,
                user_id=user_id # Passa o user_id para o construtor do Log
            )
            db.session.add(new_log)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            # Este é o erro que você está vendo:
            print(f"CRITICAL: Error in LogService.create_log: {e}")
            # Não vamos mais levantar o erro, para não quebrar a requisição principal
            # raise e
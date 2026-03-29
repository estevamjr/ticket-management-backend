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
    def create_log(action: str, details: str, user_id: str = None):
        try:
            new_log = Log(
                action=action, 
                details=details,
                user_id=user_id 
            )
            db.session.add(new_log)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"CRITICAL: Error in LogService.create_log: {e}")
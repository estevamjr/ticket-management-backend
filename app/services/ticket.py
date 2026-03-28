from app.extensions import db
from app.models.ticket import Ticket
from app.models.user import User 

class TicketService:
    @staticmethod 
    def create(data, creator_id): 
        try:
            title = data['title']
            if not User.query.get(creator_id): return "USER_NOT_FOUND" 
            
            if title.startswith('[IA]'):
                existing = Ticket.query.filter_by(title=title, status='Open').first()
                if existing: return existing
                
            new_t = Ticket(
                title=title, 
                description=data['description'], 
                user_id=creator_id, 
                status='Open', 
                priority=data['priority']
            )
            
            db.session.add(new_t)
            db.session.commit()
            return new_t
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_status(ticket_id, new_status):
        try:
            ticket = Ticket.query.get(ticket_id)
            if ticket:
                ticket.status = new_status
                db.session.commit()
                return ticket
            return None
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def getAll():
        return Ticket.query.options(db.joinedload(Ticket.creator)).order_by(Ticket.priority.desc()).all()

    @staticmethod
    def deleteFisical(tid):
        t = Ticket.query.get(tid)
        if t: 
            db.session.delete(t)
            db.session.commit()
            return True
        return False

    @staticmethod
    def getById(tid):
        return Ticket.query.get(tid)

__all__ = [
    "TicketService",
]
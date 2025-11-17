from app.extensions import db
from app.models.ticket import Ticket
from app.models.user import User 

class TicketService:
    
    @staticmethod 
    def create(data: dict, creator_id: str) -> Ticket: 
        try:
            user_id = creator_id 
            title = data['title']

            creator = User.query.get(user_id)
            if not creator:
                return "USER_NOT_FOUND" 

            if Ticket.query.filter_by(title=title).first():
                return None

            newRegister = Ticket(
                title=title, 
                description=data['description'], 
                user_id=user_id,
                status='Open',
                priority=data['priority'],
                assignee_id=None
            )
            db.session.add(newRegister)
            db.session.commit()
            return newRegister
            
        except Exception as e:
            db.session.rollback()
            print(f"Error in DB: {e}")
            raise e
    
    @staticmethod
    def deleteFisical(ticketId: str) -> bool:
        try:
            ticket = Ticket.query.get(ticketId)
            if ticket:
                db.session.delete(ticket)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error in DB when delete {ticketId}: {e}")
            raise e
    
    @staticmethod
    def getAll() -> list[Ticket]:
        try:
            return Ticket.query.options(
                db.joinedload(Ticket.creator),
                db.joinedload(Ticket.assignee)
            ).order_by(Ticket.priority.desc()).all()
        except Exception as e:
            print(f"Error in DB: {e}")
            raise e
        
    @staticmethod
    def getById(ticketId: str) -> Ticket | None:
        try:
            return Ticket.query.get(ticketId)
        except Exception as e:
            print(f"Error in DB: {e}")
            raise e    
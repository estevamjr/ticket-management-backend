from flask import request
from flask_restful import Resource, Api
from app.services.ticket import TicketService
from app.services.log import LogService
from app.utils.httpResponses import (
    success_200, 
    success_201, 
    error_400, 
    error_404, 
    error_409, 
    error_500
)
from app.utils.log import *
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity 
)
from app.models.ticket import Ticket 
from app.schemas.ticket import TicketSchema 

def initializeRoutes(api: Api):
    api.add_resource(
        TicketResource, 
        '/tickets', 
        '/tickets/<string:ticketId>'
    )
    api.add_resource(
        TicketListResource, 
        '/tickets/list'
    )

class TicketResource(Resource):
    
    @jwt_required() 
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()

            requiredFields = [
                'title', 
                'description', 
                'priority'
            ]
            if not all(field in data for field in requiredFields):
                missing = [f for f in requiredFields if f not in data]
                return error_400(f"Missing required fields: {', '.join(missing)}")

            ticket = TicketService.create(
                data, 
                creator_id=current_user_id
            ) 

            if ticket == "USER_NOT_FOUND":
                return error_404("User (creator) not found. Invalid token.")
            if ticket is None:
                LogService.create_log(
                    "CREATE_TICKET_ERROR", 
                    ticket_already_exists(data['title']), 
                    user_id=current_user_id
                )
                return error_409(ticket_already_exists(data['title']))

            LogService.create_log(
                "CREATE_TICKET_SUCCESS", 
                create_ticket_success(
                    ticket.id, 
                    ticket.title
                ), 
                user_id=current_user_id
            )
            ticket_schema = TicketSchema()
            ticket_data = ticket_schema.dump(ticket)
            return success_201(ticket_data)

        except Exception as e:
            user_id_on_error = None
            try: user_id_on_error = get_jwt_identity()
            except: pass
            LogService.create_log(
                "CREATE_TICKET_ERROR", 
                create_ticket_error(
                    e, 
                    data.get(
                        'title', 
                        'N/A'
                    )
                ), 
                user_id=user_id_on_error
            )
            return error_500(str(e))

    @jwt_required() 
    def delete(self, ticketId):
        try:
            current_user_id = get_jwt_identity() # Pegar o ID do usuário
            ticket = TicketService.getById(ticketId)
            
            if not ticket:
                LogService.create_log(
                    "DELETE_TICKET_ERROR", 
                    delete_ticket_error_404(ticketId), 
                    user_id=current_user_id
                )
                return error_404(delete_ticket_error_404(ticketId))

            if TicketService.deleteFisical(ticketId):
                LogService.create_log(
                    "DELETE_TICKET_SUCCESS", 
                    delete_ticket_success(
                        ticket.id, 
                        ticket.title
                    ), 
                    user_id=current_user_id
                )
                return success_200(message=f"Ticket {ticketId} deleted")
            
            raise Exception("Delete failed")

        except Exception as e:
            user_id_on_error = None
            try: user_id_on_error = get_jwt_identity()
            except: pass
            LogService.create_log(
                "DELETE_TICKET_ERROR", 
                delete_ticket_error_500(
                    e, 
                    ticketId
                ), 
                user_id=user_id_on_error
            )
            return error_500(delete_ticket_error_500(e, ticketId))

    @jwt_required() 
    def get(self, ticketId):
        try:
            ticket = TicketService.getById(ticketId)
            if ticket:
                return success_200(ticket)
            
            return error_404(ticket_not_found(ticketId))
        except Exception as e:
            user_id_on_error = None
            try: user_id_on_error = get_jwt_identity()
            except: pass
            LogService.create_log(
                "GET_TICKET_ERROR", 
                get_ticket_error(
                    e, 
                    ticketId
                ),
                user_id=user_id_on_error
            )
            return error_500(str(e))

class TicketListResource(Resource):
    
    @jwt_required() 
    def get(self):
        try:
            tickets = TicketService.getAll()
            schema = TicketSchema(many=True)
            return success_200(schema.dump(tickets)) 
        
        except Exception as e:
            user_id_on_error = None
            try: user_id_on_error = get_jwt_identity()
            except: pass
            LogService.create_log(
                "GET_ALL_TICKETS_ERROR", 
                get_all_tickets_error(e), 
                user_id=user_id_on_error
            )
            return error_500("An error occurred while processing your request to list tickets")
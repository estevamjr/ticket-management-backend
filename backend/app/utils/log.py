def create_ticket_success(ticket_id: str, title: str) -> str:
    return f"Ticket '{title}' (ID: {ticket_id[:8]}...) was created."

def create_ticket_error(e: Exception, title: str) -> str:
    return f"Error creating ticket '{title}'. Exception: {e}"

def delete_ticket_success(ticket_id: str, title: str) -> str:
    return f"Ticket '{title}' (ID: {ticket_id[:8]}...) was deleted."

def delete_ticket_error_404(ticket_id: str) -> str:
    return f"Ticket with ID {ticket_id} was not found for deletion."

def delete_ticket_error_500(e: Exception, ticket_id: str) -> str:
    return f"Error deleting ticket {ticket_id}. Exception: {e}"

def get_ticket_error(e: Exception, ticket_id: str) -> str:
    return f"Error retrieving ticket {ticket_id}. Exception: {e}"

def get_all_tickets_error(e: Exception) -> str:
    return f"Error retrieving all tickets. Exception: {e}"

def get_all_tickets_success() -> str:
    return "Tickets listed successfully."

def ticket_not_found(ticket_id: str) -> str:
    return f"Ticket with ID {ticket_id} was not found."

def ticket_already_exists(title: str) -> str:
    return f"Ticket with title '{title}' already exists."

def login_success(username: str, user_id: str) -> str:
    return f"User '{username}' (ID: {user_id}) logged in successfully."

def login_failed_401(username: str) -> str:
    return f"Error: User '{username}' not found or incorrect password."
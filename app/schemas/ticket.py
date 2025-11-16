#
# COPIE E COLE ISSO EM: app/schemas/ticket.py
#
from datetime import datetime
from typing import List

from marshmallow import Schema, fields, validate, EXCLUDE
from app.extensions import ma # Necessário para o fields.Nested

def _set_field_default(field: fields.Field, value):
    """Set default/load default/missing on a field for cross-version compatibility."""
    for attr in ("missing", "load_default", "default"):
        try:
            setattr(field, attr, value)
        except Exception:
            pass

# --- SCHEMA DE USUÁRIO CORRIGIDO ---
class UserSchema(Schema):
    """Public representation of a user."""
    # CORREÇÃO: O ID no seu model 'user.py' é String(36)
    id = fields.String(dump_only=True, metadata={"description": "Database ID of the user (UUID)"}) 
    username = fields.Str(required=True, metadata={"description": "Username"})

    class Meta:
        ordered = True
        unknown = EXCLUDE

# --- SCHEMA BASE DO TICKET CORRIGIDO ---
class TicketBaseSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        metadata={"description": "Short title for the ticket"},
    )
    description = fields.Str(allow_none=True, metadata={"description": "Detailed description of the ticket"})
    status = fields.Str(metadata={"description": "Ticket status (e.g. open, in_progress, closed)"})
    _set_field_default(status, "Aberto") # Usando o status do seu frontend

    # CORREÇÃO: A prioridade no seu frontend é String
    priority = fields.Str(
        validate=validate.OneOf(["Baixa", "Média", "Alta"]),
        metadata={"description": "Prioridade (Baixa, Média, Alta)"},
    )
    _set_field_default(priority, "Baixa")

    tags = fields.List(fields.Str(), metadata={"description": "Optional list of tags"})
    _set_field_default(tags, list)

    due_date = fields.DateTime(allow_none=True, metadata={"description": "Optional due date/time for the ticket"})

    class Meta:
        ordered = True
        unknown = EXCLUDE

# --- SCHEMA DE CRIAÇÃO CORRIGIDO ---
class TicketCreateSchema(TicketBaseSchema):
    # CORREÇÃO: O 'reporter_id' (ou user_id) NÃO é mais necessário aqui.
    # Ele virá do token JWT, como corrigimos no app/controllers/ticket.py
    
    # CORREÇÃO: O ID do assignee é String
    assignee_id = fields.String(allow_none=True, metadata={"description": "User ID (UUID) assigned to work the ticket"})

# --- SCHEMA DE UPDATE CORRIGIDO ---
class TicketUpdateSchema(Schema):
    """Payload accepted when updating a ticket - all fields optional for partial updates."""
    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    status = fields.Str()
    priority = fields.Str(validate=validate.OneOf(["Baixa", "Média", "Alta"]))
    tags = fields.List(fields.Str())
    due_date = fields.DateTime(allow_none=True)
    # CORREÇÃO: O ID do assignee é String
    assignee_id = fields.String(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE

# --- SCHEMA DE DB CORRIGIDO ---
class TicketInDBBaseSchema(TicketBaseSchema):
    """Fields stored in DB and sent to clients."""

    # CORREÇÃO: Todos os IDs são String
    id = fields.String(required=True, metadata={"description": "Database ID of the ticket (UUID)"})
    # CORREÇÃO: O nome do campo no model 'ticket.py' é 'user_id'
    user_id = fields.String(allow_none=True) 
    assignee_id = fields.String(allow_none=True)
    
    created_at = fields.DateTime()
    _set_field_default(created_at, lambda: datetime.utcnow())
    updated_at = fields.DateTime(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE

# --- SCHEMA DE RETORNO CORRIGIDO ---
class TicketSchema(TicketInDBBaseSchema):
    """Public representation of a ticket."""
    
    # CORREÇÃO: Adicionando o campo 'creator' (que é o nome da 
    # Relação no 'ticket.py') para que o 'joinedload' funcione.
    creator = fields.Nested(UserSchema, dump_only=True)
    assignee = fields.Nested(UserSchema, dump_only=True, allow_none=True)


# Backwards-compatible exports
__all__ = [
    "TicketBaseSchema",
    "TicketCreateSchema",
    "TicketUpdateSchema",
    "TicketInDBBaseSchema",
    "TicketSchema",
]
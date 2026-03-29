from datetime import datetime
from typing import List
from marshmallow import Schema, fields, validate, EXCLUDE
from app.extensions import ma 
from app.models.log import Log

def _set_field_default(field: fields.Field, value):
    for attr in (
        "missing", 
        "load_default", 
        "default"):
        
        try:
            setattr(field, attr, value)
        except Exception:
            pass

class UserSchema(Schema):
    id = fields.String(
        dump_only=True, 
        metadata={"description": "Database ID of the user (UUID)"}
    )
     
    username = fields.Str(
        required=True, 
        metadata={"description": "Username"}
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE

class TicketBaseSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        metadata={"description": "Short title for the ticket"},
    )
    description = fields.Str(
        allow_none=True, 
        metadata={"description": "Detailed description of the ticket"}
    )
    status = fields.Str(metadata={"description": "Ticket status (e.g. open, in_progress, closed)"})
    _set_field_default(
        status, 
        "Open"
    )

    priority = fields.Str(
        validate=validate.OneOf(["Low", "Middle", "High"]),
        metadata={"description": "Prioridade (Low, Middle, High)"},
    )
    _set_field_default(
        priority, 
        "High"
    )

    tags = fields.List(fields.Str(), metadata={"description": "Optional list of tags"})
    _set_field_default(tags, list)

    due_date = fields.DateTime(
        allow_none=True, 
        metadata={"description": "Optional due date/time for the ticket"}
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE

class TicketCreateSchema(TicketBaseSchema):
    
    assignee_id = fields.String(
        allow_none=True, 
        metadata={"description": "User ID (UUID) assigned to work the ticket"}
    )

class TicketUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    status = fields.Str()
    priority = fields.Str(validate=validate.OneOf(["Low", "Middle", "High"]))
    tags = fields.List(fields.Str())
    due_date = fields.DateTime(allow_none=True)
    assignee_id = fields.String(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE

class TicketInDBBaseSchema(TicketBaseSchema):
    id = fields.String(required=True, metadata={"description": "Database ID of the ticket (UUID)"})
    user_id = fields.String(allow_none=True) 
    assignee_id = fields.String(allow_none=True)
    
    created_at = fields.DateTime()
    _set_field_default(created_at, lambda: datetime.utcnow())
    updated_at = fields.DateTime(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE

class TicketSchema(TicketInDBBaseSchema):
    creator = fields.Nested(UserSchema, dump_only=True)
    assignee = fields.Nested(UserSchema, dump_only=True, allow_none=True)
    
class LogSchema(Schema):
    id = fields.Str(
        required=True, 
        metadata={"description": "UUID do registro de log"}
    )
    timestamp = fields.DateTime(
        required=True, 
        metadata={"description": "Data e hora do evento"}
    )
    
    action = fields.Str(
        required=True, 
        metadata={"description": "Tipo de ação (ex: CREATE_TICKET_SUCCESS)"}
    )
    
    details = fields.Str(
        allow_none=True, 
        metadata={"description": "Detalhes da ação executada"}
    )

    class Meta:
        model = Log 
        ordered = True
        unknown = EXCLUDE    

__all__ = [
    "TicketBaseSchema",
    "TicketCreateSchema",
    "TicketUpdateSchema",
    "TicketInDBBaseSchema",
    "TicketSchema",
]
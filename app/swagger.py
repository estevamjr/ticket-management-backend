from typing import Dict, Any
from marshmallow import Schema, fields

from app.schemas.ticket import (
    TicketCreateSchema,
    TicketSchema,
    UserSchema,
    LogSchema, 
)


FIELD_TYPE_MAP = {
    'String': ('string', None),
    'Integer': ('integer', 'int32'),
    'Float': ('number', 'float'),
    'Boolean': ('boolean', None),
    'DateTime': ('string', 'date-time'),
    'List': ('array', None),
}


def _field_to_schema(field: fields.Field) -> Dict[str, Any]:
    fname = field.__class__.__name__
    if fname == 'List':
        inner = getattr(field, 'inner', None)
        item_schema = _field_to_schema(inner) if inner is not None else {'type': 'string'}
        return {'type': 'array', 'items': item_schema}

    otype, format_ = FIELD_TYPE_MAP.get(fname, ('string', None))
    schema: Dict[str, Any] = {'type': otype}
    if format_:
        schema['format'] = format_
    return schema


def _schema_to_definition(schema_cls: Schema) -> Dict[str, Any]:
    schema = schema_cls()
    props: Dict[str, Any] = {}
    required = []
    for name, field in schema.fields.items():
        props[name] = _field_to_schema(field)
        if getattr(field, 'required', False):
            required.append(name)

    definition: Dict[str, Any] = {'type': 'object', 'properties': props}
    if required:
        definition['required'] = required
    return definition


def build_swagger_template() -> Dict[str, Any]:
    
    definitions = {
        'Ticket': _schema_to_definition(TicketSchema),
        'TicketCreate': _schema_to_definition(TicketCreateSchema),
        'User': _schema_to_definition(UserSchema),
        'Log': _schema_to_definition(LogSchema), # <--- NOVO
    }

    template: Dict[str, Any] = {
        'swagger': '2.0',
        'info': {
            'title': 'Ticket Management API',
            'version': '0.0.1',
        },
        'definitions': definitions,
        'securityDefinitions': {
            'bearerAuth': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'",
            }
        },
        'paths': {
            '/tickets': {
                'post': {
                    'tags': ['Tickets'],
                    'summary': 'Creates a new ticket in the system.', 
                    'security': [{'bearerAuth': []}],
                    'parameters': [
                        {
                            'in': 'body',
                            'name': 'body',
                            'required': True,
                            'schema': {'$ref': '#/definitions/TicketCreate'},
                        }
                    ],
                    'responses': {
                        '201': {'description': 'Ticket created', 'schema': {'$ref': '#/definitions/Ticket'}},
                        '400': {'description': 'Missing or invalid fields'},
                        '401': {'description': 'Unauthorized'}, 
                        '500': {'description': 'Internal server error'},
                    },
                }
            },
            '/auth': {
                'post': {
                    'tags': ['Auth'],
                    'summary': 'Authenticates a user and returns the JWT.', 
                    'parameters': [
                        {
                            'in': 'body',
                            'name': 'body',
                            'required': True,
                            'schema': {
                                'type': 'object',
                                'required': ['username', 'password'],
                                'properties': {
                                    'username': {'type': 'string'},
                                    'password': {'type': 'string'},
                                },
                            },
                        }
                    ],
                    'responses': {
                        '200': {
                            'description': 'Returns access token and user data.', 
                            'schema': {'type': 'object', 'properties': {'access_token': {'type': 'string'}}},
                        },
                        '400': {'description': 'Missing fields'},
                        '401': {'description': 'Invalid credentials'},
                        '500': {'description': 'Internal server error'},
                    },
                }
            },
            '/users/register': {
                'post': {
                    'tags': ['Auth'],
                    'summary': 'Registers a new user in the system.', 
                    'parameters': [
                        {
                            'in': 'body',
                            'name': 'body',
                            'required': True,
                            'schema': {
                                'type': 'object',
                                'required': ['username', 'password'],
                                'properties': {
                                    'username': {'type': 'string'},
                                    'password': {'type': 'string'},
                                },
                            }
                        }
                    ],
                    'responses': {
                        '201': {'description': 'User created', 'schema': {'$ref': '#/definitions/User'}},
                        '400': {'description': 'Missing or invalid fields'},
                        '409': {'description': 'User already exists'},
                        '500': {'description': 'Internal server error'},
                    },
                }
            },
            '/tickets/list': {
                'get': {
                    'tags': ['Tickets'],
                    'summary': 'Returns the list of all open tickets.', 
                    'security': [{'bearerAuth': []}],
                    'responses': {
                        '200': {'description': 'A list of tickets', 'schema': {'type': 'array', 'items': {'$ref': '#/definitions/Ticket'}}},
                        '404': {'description': 'No tickets found (Deprecated, returns 200/empty list)'},
                        '401': {'description': 'Unauthorized'},
                        '500': {'description': 'Internal server error'},
                    },
                }
            },
            '/logs': {
                'get': {
                    'tags': ['Logs'],
                    'summary': 'Returns the list of system activity logs.', 
                    'security': [{'bearerAuth': []}],
                    'responses': {
                        '200': {
                            'description': 'The list of activity logs was returned successfully.', 
                            'schema': {'type': 'array', 'items': {'$ref': '#/definitions/Log'}}
                        },
                        '401': {'description': 'Unauthorized'},
                        '404': {'description': 'No logs found.'},
                        '500': {'description': 'Internal server error'},
                    },
                }
            },
            '/tickets/{ticket_id}': {
                'parameters': [
                    {'name': 'ticket_id', 'in': 'path', 'required': True, 'type': 'string'}
                ],
                'get': {
                    'tags': ['Tickets'],
                    'summary': 'Retrieves a specific ticket by ID.', 
                    'security': [{'bearerAuth': []}],
                    'responses': {
                        '200': {'description': 'Ticket retrieved', 'schema': {'$ref': '#/definitions/Ticket'}},
                        '404': {'description': 'Ticket not found'},
                        '401': {'description': 'Unauthorized'},
                        '500': {'description': 'Internal server error'},
                    },
                },
                'delete': {
                    'tags': ['Tickets'],
                    'summary': 'Deletes a specific ticket by ID.', 
                    'security': [{'bearerAuth': []}],
                    'responses': {
                        '200': {'description': 'Ticket deleted'},
                        '404': {'description': 'Ticket not found'},
                        '401': {'description': 'Unauthorized'},
                        '500': {'description': 'Internal server error'},
                    },
                },
            },
        },
    }

    return template
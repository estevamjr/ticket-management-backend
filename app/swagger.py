"""Build a minimal OpenAPI template from Marshmallow schemas.

This module creates an OpenAPI template dict using the Marshmallow
schemas defined in `app.schemas`. It intentionally avoids changing
controllers: no YAML docstrings are required in resource methods.

We only implement a small type mapper sufficient for the Ticket schemas.
If you add more schemas, extend `FIELD_TYPE_MAP` or add custom handling.
"""
from typing import Dict, Any
from marshmallow import Schema, fields

from app.schemas.ticket import (
    TicketCreateSchema,
    TicketSchema,
    UserSchema,
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
    """Convert a Marshmallow field to a JSON Schema fragment."""
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
    """Create an OpenAPI schema definition from a Marshmallow Schema class."""
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
    """Return an OpenAPI template dict ready to pass to Flasgger.

    This includes components/schemas and a small set of path definitions for
    the ticket endpoints used by this app.
    """
    definitions = {
        'Ticket': _schema_to_definition(TicketSchema),
        'TicketCreate': _schema_to_definition(TicketCreateSchema),
        'User': _schema_to_definition(UserSchema),
    }

    # Use Swagger 2.0 format because Flasgger may merge in a `swagger: "2.0"`
    # field internally; producing a v2 template avoids the "swagger and openapi"
    # fields conflict when Flasgger renders the UI.
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
                        '500': {'description': 'Internal server error'},
                    },
                }
            },
            '/auth': {
                'post': {
                    'tags': ['Auth'],
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
                            'description': 'Returns access token',
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
                                    'password': {'type': 'string', 'format': 'password'},
                                },
                            },
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
                    'security': [{'bearerAuth': []}],
                    'responses': {
                        '200': {'description': 'A list of tickets', 'schema': {'type': 'array', 'items': {'$ref': '#/definitions/Ticket'}}},
                        '404': {'description': 'No tickets found'},
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
                    'security': [{'bearerAuth': []}],
                    'responses': {
                        '200': {'description': 'Ticket retrieved', 'schema': {'$ref': '#/definitions/Ticket'}},
                        '404': {'description': 'Ticket not found'},
                        '500': {'description': 'Internal server error'},
                    },
                },
                'delete': {
                    'tags': ['Tickets'],
                    'security': [{'bearerAuth': []}],
                    'responses': {
                        '200': {'description': 'Ticket deleted'},
                        '404': {'description': 'Ticket not found'},
                        '500': {'description': 'Internal server error'},
                    },
                },
            },
        },
    }

    return template

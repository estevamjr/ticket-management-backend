from typing import Dict, Any
from marshmallow import Schema, fields
from app.schemas.ticket import TicketCreateSchema, TicketSchema, UserSchema, LogSchema
from app.schemas.andon import AndonAnalysisSchema

# Mapeamento para tipos Swagger
FIELD_TYPE_MAP = {
    'String': ('string', None), 'Integer': ('integer', 'int32'),
    'Float': ('number', 'float'), 'DateTime': ('string', 'date-time'),
}

def _schema_to_definition(schema_cls: Schema) -> Dict[str, Any]:
    schema = schema_cls()
    props = {}
    for name, field in schema.fields.items():
        fname = field.__class__.__name__
        otype, format_ = FIELD_TYPE_MAP.get(fname, ('string', None))
        props[name] = {'type': otype}
        if format_: props[name]['format'] = format_
    return {'type': 'object', 'properties': props}

def build_swagger_template() -> Dict[str, Any]:
    definitions = {
        'Ticket': _schema_to_definition(TicketSchema),
        'TicketCreate': _schema_to_definition(TicketCreateSchema),
        'Log': _schema_to_definition(LogSchema),
        'AndonAnalysis': _schema_to_definition(AndonAnalysisSchema),
    }

    template = {
        'swagger': '2.0',
        'info': {'title': 'Agile Bison API', 'version': '1.0.0'},
        'definitions': definitions,
        'securityDefinitions': {
            'bearerAuth': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
        },
        'paths': {
            '/api/andon/analyze': {
                'post': {
                    'tags': ['Andon AI'],
                    'security': [{'bearerAuth': []}],
                    'parameters': [{'in': 'body', 'name': 'body', 'schema': {'$ref': '#/definitions/AndonAnalysis'}}],
                    'responses': {'201': {'schema': {'$ref': '#/definitions/AndonAnalysis'}}}
                }
            },
            # ... caminhos de /auth, /tickets e /logs conforme já definidos
        }
    }
    return template
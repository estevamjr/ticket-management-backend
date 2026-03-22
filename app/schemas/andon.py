from marshmallow import Schema, fields, EXCLUDE

class AndonAnalysisSchema(Schema):
    # Campos que o sensor envia
    device_id = fields.Str(required=True, metadata={"description": "ID do dispositivo/máquina"})
    cpu_usage_pct = fields.Float(required=True, metadata={"description": "Percentual de uso da CPU"})
    mem_available_gb = fields.Float(required=True, metadata={"description": "Memória RAM disponível em GB"})
    active_threats = fields.Int(required=True, metadata={"description": "Quantidade de ameaças detectadas"})
    untrusted_processes = fields.Int(required=True, metadata={"description": "Processos não confiáveis rodando"})
    
    # Campos que retornamos (extraídos do Log Model)
    id = fields.Str(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)
    andon_status = fields.Int(dump_only=True, metadata={"description": "Veredito da IA (0-Normal, 1-Warning, 2-Critical)"})

    class Meta:
        ordered = True
        unknown = EXCLUDE

__all__ = [
    "AndonAnalysisSchema",
]
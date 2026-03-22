from app.extensions import db
from app.models.log import Log
from app.ml_logic.predictor import AndonPredictor

# Inicializa o motor de IA (Singleton)
ai_engine = AndonPredictor()

class AndonService:
    @staticmethod
    def analyze_telemetry(data: dict) -> Log:
        try:
            # Executa a predição matemática
            prediction = ai_engine.predict(
                cpu=float(data['cpu_usage_pct']),
                ram=float(data['mem_available_gb']),
                threats=int(data['active_threats']),
                untrusted=int(data['untrusted_processes'])
            )

            # Persiste os dados e o resultado da IA
            new_entry = Log(
                action="AI_ANDON_ANALYSIS",
                details=f"Device: {data.get('device_id')}",
                cpu_usage=data['cpu_usage_pct'],
                ram_usage=data['mem_available_gb'],
                active_threats=data['active_threats'],
                untrusted_processes=data['untrusted_processes'],
                andon_status=prediction
            )

            db.session.add(new_entry)
            db.session.commit()
            return new_entry

        except Exception as e:
            db.session.rollback()
            raise e
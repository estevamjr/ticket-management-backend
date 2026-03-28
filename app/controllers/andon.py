from flask import request
from flask_restful import Resource, Api
from app.services.andon import AndonService
from app.services.log import LogService
from app.utils.httpResponses import success_201, error_400, error_500
from app.schemas.andon import AndonAnalysisSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

def initializeAndonRoutes(api: Api):
    api.add_resource(AndonResource, '/api/andon/analyze')

class AndonResource(Resource):
    
    @jwt_required() 
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()

            required = [
                'device_id', 
                'cpu_usage_pct', 
                'mem_available_gb', 
                'active_threats', 
                'untrusted_processes'
            ]
            
            if not all(field in data for field in required):
                return error_400("Missing required telemetry fields")

            analysis_log = AndonService.analyze_telemetry(data)

            LogService.create_log(
                "AI_ANDON_ANALYSIS", 
                f"Analysis for device: {data['device_id']} - Status: {analysis_log.andon_status}", 
                user_id=current_user_id
            )

            schema = AndonAnalysisSchema()
            return success_201(schema.dump(analysis_log))

        except Exception as e:
            user_id = None
            try: user_id = get_jwt_identity()
            except: pass
            LogService.create_log("AI_ANALYSIS_ERROR", str(e), user_id=user_id)
            return error_500(f"AI Engine Error: {str(e)}")
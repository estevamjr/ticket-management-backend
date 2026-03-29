from app.models.ticket import Ticket
from app.models.user import User

def success_200(data=None, message="Success"):
    response = {
        "success": True,
        "message": message
    }
    
    if data is None:
        return response, 200

    if isinstance(data, dict):
        response.update(data)
        
    elif isinstance(data, list):
        json_list = []
        for item in data:
            if hasattr(item, 'to_json'):
                json_list.append(item.to_json())
            else:
                json_list.append(item)
        response["data"] = json_list
        
    elif hasattr(data, 'to_json'):
        response["data"] = data.to_json()
        
    else:
        response["data"] = data

    return response, 200

def success_201(data, message="Resource created successfully"):
    return {
        "success": True,
        "message": message,
        "data": data 
    }, 201

def error_400(details="Missing required fields"):
    return {
        "success": False,
        "error": "Bad Request",
        "message": details
    }, 400
    
def error_401(message="Unauthorized access"):
    return {
        "success": False,
        "error": "Unauthorized",
        "message": message
    }, 401    

def error_404(message="Resource not found"):
    return {
        "success": False,
        "error": "Not Found",
        "message": message
    }, 404

def error_409(message="Resource already exists"):
    return {
        "success": False,
        "error": "Conflict",
        "message": message
    }, 409

def error_500(message="An error occurred while processing your request."):
    return {
        "success": False,
        "error": "Internal Server Error",
        "message": message
    }, 500

def error_504(message="The request timed out."):
    return {
        "success": False,
        "error": "Gateway Timeout",
        "message": message
    }, 504
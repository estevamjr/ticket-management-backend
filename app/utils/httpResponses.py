#
# COPIE E COLE ISSO EM: app/utils/httpResponses.py
#
from app.models.ticket import Ticket
from app.models.user import User

def success_200(data=None, message="Success"):
    response = {
        "success": True,
        "message": message
    }
    
    if data is None:
        return response, 200

    # SE 'data' FOR UM DICIONÁRIO (EX: LOGIN COM TOKEN)
    if isinstance(data, dict):
        response.update(data)
        
    # Se 'data' for uma LISTA (EX: GET /tickets/list)
    elif isinstance(data, list):
        json_list = []
        # O FOR loop garante que o .to_json() não seja chamado na lista inteira
        for item in data:
            # Se for um objeto Model (que tem to_json), serializa
            if hasattr(item, 'to_json'):
                json_list.append(item.to_json())
            # Se já for um dicionário (do schema.dump), apenas adiciona
            else:
                json_list.append(item)
        response["data"] = json_list
        
    # Se 'data' for um ÚNICO objeto Model 
    elif hasattr(data, 'to_json'):
        response["data"] = data.to_json()
        
    else:
        response["data"] = data

    return response, 200
    """
    Retorno 200 genérico.
    Mescla dicionários (como tokens/listas serializadas) diretamente na resposta.
    """
    response = {
        "success": True,
        "message": message
    }
    
    if data is None:
        return response, 200

    # SE 'data' FOR UM DICIONÁRIO (EX: LOGIN COM TOKEN)
    if isinstance(data, dict):
        response.update(data)
        
    # Se 'data' for uma LISTA de objetos (Modelos ou Dicionários serializados)
    elif isinstance(data, list):
        json_list = []
        for item in data:
            # Se for um objeto Model (que tem to_json), serializa
            if hasattr(item, 'to_json'):
                json_list.append(item.to_json())
            # Se já for um dicionário (do schema.dump), apenas adiciona
            else:
                json_list.append(item)
        response["data"] = json_list # Renomeado para 'data'
        
    # Se 'data' for um ÚNICO objeto Model (que tem to_json)
    elif hasattr(data, 'to_json'):
        response["data"] = data.to_json()
        
    else:
        response["data"] = data

    return response, 200


def success_201(data, message="Resource created successfully"):
    """
    Retorno 201 genérico. O frontend espera 'data' neste formato.
    """
    return {
        "success": True,
        "message": message,
        # O data já é um dicionário serializado do schema.dump()
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
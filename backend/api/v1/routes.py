from fastapi import APIRouter, Request
from backend.algorithm import Algorithm
from backend.services.user_service import UserService
from backend.core.exceptions import ApiException
from backend.utils.logging_utils import *
from backend.database.managers.database_manager import DatabaseManager

router = APIRouter()

@router.post("/auth/create")
async def handle_oauth(request: Request):
    """
    Handle OAuth user data storage.
    
    Args:
        request: The incoming request
        
    Returns:
        HTTP response with operation result
    """
    try:
        body = await request.json()
        db_manager  = DatabaseManager.get_instance()
        user_service_instance = UserService(db_manager, body)
        response = await user_service_instance.handle_request()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"OAuth handling error: {str(error)}")
        return error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in OAuth handler: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing OAuth request",
            data=str(e)
        )


# API endpoint to trigger the autorun algorithm
# Triggers the autorun trading algorithm.
# @return A message indicating the success or failure of the algorithm start.
@router.get("/autorun")
async def trigger_algo():
    """
    Triggers the autorun algorithm.

    Returns:
        dict: A message indicating the success or failure of the algorithm start.
    """
    try:
        application = ALGORITHM_PATH()
        await application.autorun()
        return {"message": "Algo started successfully"}
    except Exception as error:
        return {"error": str(error)}

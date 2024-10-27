from fastapi import APIRouter, Request
from backend.autorun import Algo
from backend.services.register_service import Register
from backend.services.login_service import Login
from backend.services.forgot_password_service import ForgotPassword
from backend.core.exceptions import ApiException
from backend.utils.logging_utils import *

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    """
    Handles user registration.

    Args:
        request (Request): The HTTP request containing user registration data.

    Returns:
        HTTPResponse: The response object containing the result of the registration process.
    """
    try:
        body = await request.json()
        register_object = Register(body)
        response = register_object.handle_request()
        return response.to_http_response()
    except ApiException as error:
        return error.to_http_exception()
    except Exception as error:
        return  ApiException.internal_server_error(str(error)).to_http_exception()

@router.post("/login")
async def login(request: Request):
    """
    Handles user login.

    Args:
        request (Request): The HTTP request containing user login data.

    Returns:
        HTTPResponse: The response object containing the result of the login process.
    """
    try:
        body = await request.json()
        login_object = Login(body)
        response = login_object.handle_request()
        return response.to_http_response()
    except ApiException as error:
        return error.to_http_exception()
    except Exception as error:
        return  ApiException.internal_server_error(str(error)).to_http_exception()

@router.post("/forgot-password")
async def forgot_password(request: Request):
    """
    Handles the forgot password process.

    Args:
        request (Request): The HTTP request containing user email for password recovery.

    Returns:
        HTTPResponse: The response object containing the result of the password recovery process.
    """
    try:
        body = await request.json()
        forgot_password_object = ForgotPassword(body)
        response = forgot_password_object.handle_request()
        return response.to_http_response()
    except ApiException as error:
        return error.to_http_exception()
    except Exception as error:
        return  ApiException.internal_server_error(str(error)).to_http_exception()

@router.get("/autorun")
async def trigger_algo():
    """
    Triggers the autorun algorithm.

    Returns:
        dict: A message indicating the success or failure of the algorithm start.
    """
    try:
        application = Algo()
        await application.autorun()
        return {"message": "Algo started successfully"}
    except Exception as error:
        return {"error": str(error)}

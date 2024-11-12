import jwt

from backend.models.users_model import UsersModel
from backend.database.schemas.authentication_schema import ForgotPasswordSchema

from backend.services.BaseService import BaseService
from backend.services.email_service import EmailService

from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse

from datetime import datetime, timedelta, timezone 

from backend.utils.logging_utils import *
from backend.enumerations.enums import *
from backend.constants.const import *


class ForgotPasswordService(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = ForgotPasswordSchema(**request)


    async def handle_request(self):
        # Extract Input Parameters
        user_email = self.request_parameters.user_email

        # Verify Registered User
        await self.verify_registered_user(user_email)

        # Generate a secure token
        user_password_reset_token = self.generate_password_reset_token(user_email)
        
        # Save the token 
        await self.save_password_reset_token(user_email, user_password_reset_token)

        # Send an email with the token 
        send_email = self.send_password_reset_email(user_email, user_password_reset_token)

        # Return Response
        if send_email["success"]:
            return ApiResponse.success(
                message = "SERVER_FORGOT_PASSWORD_EMAIL_SENT", 
                data = {"token": user_password_reset_token}
            )
        else:
            raise ApiException.internal_server_error(
                message = "SERVER_FORGOT_PASSWORD_EMAIL_SENDING_FAILURE", 
                data = str(send_email["error"])
            )


    # Generate Forgot Password Token
    def generate_password_reset_token(self, user_email):
        expiration_time = datetime.datetime.now(timezone.utc) + timedelta(minutes=15)
        payload = {
            'user_email': user_email,
            'exp': expiration_time
        }

        try:
            jwt_token = jwt.encode(payload, SECRET_NAME, algorithm='HS256')
            return jwt_token
        except Exception as error:
            raise ApiException.internal_server_error(
                message = "SERVER_FORGOT_PASSWORD_TOKEN_GENERATION_FAILURE", 
                data = str(error)
            )


    # Verify Registered User
    async def verify_registered_user(self, user_email):
        try:
            await self.database.execute_function(
                Functions.VERIFY_USER_REGISTRATION_FN.value, user_email, multiple=False
            )
        except Exception as error:
            if str(error) == "DB_USER_NOT_FOUND":
                raise ApiException.validation_error(message="SERVER_LOGIN_EMAIL_INCORRECT")
            else:
                raise ApiException.internal_server_error(
                    message="SERVER_GET_USER_DB_FAILURE", data=str(error)
                )


    # Save Forgot Password Token
    async def save_password_reset_token(self, user_email, user_password_reset_token):     
        try:
            await self.database.execute_stored_procedure(
                Procedures.SAVE_USER_PASSWORD_RESET_TOKEN_SP.value, 
                user_email, 
                user_password_reset_token
            )
        except Exception as error:
            raise ApiException.internal_server_error(
                message="SERVER_PASSWORD_RESET_TOKEN_DB_FAILURE", data=str(error)
            )


    # Send Forgot Password Email
    def send_password_reset_email(self, user_email, user_password_reset_token):
        email_object = EmailService()
        send_email = email_object.send_email(
            recipient_email = user_email, 
            template = "forgot_password", 
            reset_link = f"http://localhost:5173/reset-password/token={user_password_reset_token}"
        )
        return send_email
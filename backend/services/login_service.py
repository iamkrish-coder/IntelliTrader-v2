# Login

import bcrypt
import jwt

from backend.database.models.users_model import UsersModel
from backend.database.schemas.authentication_schema import LoginSchema

from backend.services.BaseService import BaseService
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse

from backend.utils.logging_utils import *
from backend.enumerations.enums import *
from backend.constants.const import *


class LoginService(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = LoginSchema(**request)


    async def handle_request(self):
        # Extract Input Parameters
        user_email = self.request_parameters.user_email
        entered_credentials = self.request_parameters.user_password

        # Get User Registration Details
        saved_user_credentials = await self.get_registered_user_details(user_email)

        # Generate JWT Token
        login_token = self.generate_jwt_token(user_email)

        # Validate Password and Return Response
        if self.validate_password(saved_user_credentials, entered_credentials):
            return ApiResponse.success(
                message="SERVER_LOGIN_SUCCESSFUL", data={"token": login_token}
            )
        else:
            raise ApiException.validation_error(message="SERVER_INVALID_CREDENTIALS")


    # Get Registered User Details
    async def get_registered_user_details(self, user_email):
        try:
            registered_user_details = await self.database.execute_function(
                Functions.GET_USER_REGISTRATION_FN.value, user_email, multiple=False
            )
            return registered_user_details
        except Exception as error:
            if str(error) == "DB_USER_NOT_FOUND":
                raise ApiException.validation_error(message="SERVER_LOGIN_EMAIL_INCORRECT")
            else:
                raise ApiException.internal_server_error(
                    message="SERVER_GET_USER_DB_FAILURE", data=str(error)
                )


    # Generate JWT Token
    def generate_jwt_token(self, user_email):
        try:    
            payload = {"userEmail": user_email}
            jwt_token = jwt.encode(payload, SECRET_NAME, algorithm="HS256")
            return jwt_token
        except Exception as error:
            raise ApiException.internal_server_error(
                message="SERVER_GENERATE_JWT_FAILURE", data=str(error)
            )


    # Validate Password
    def validate_password(self, saved_user_credentials, entered_credentials):
        try:
            saved_user_password = saved_user_credentials["user_password"]
            return bcrypt.checkpw(
                entered_credentials.encode("utf-8"), saved_user_password.encode("utf-8")
            )
        except Exception as error:
            raise ApiException.internal_server_error(
                message="SERVER_VALIDATE_PASSWORD_FAILURE", data=str(error)
            )

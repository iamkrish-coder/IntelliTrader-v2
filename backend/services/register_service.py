# Registration

import jwt
import time
import bcrypt

from backend.database.models.users_model import UsersModel
from backend.database.schemas.authentication_schema import UsersSchema

from backend.services.BaseService import BaseService
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse

from backend.utils.logging_utils import *
from backend.enumerations.enums import *
from backend.constants.const import *


class RegisterService(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = UsersSchema(**request)


    async def handle_request(self):
        # Extract Input Parameters
        user_full_name = self.request_parameters.user_full_name
        user_email = self.request_parameters.user_email
        user_password = self.request_parameters.user_password

        # Generate JWT Token
        registration_token = self.generate_jwt_token(user_email)

        # Hash Passwords
        user_hashed_password, user_password_salt = self.hash_user_password(
            user_password
        )

        # save user to database
        save_user_response = await self.save_user_registration(
            user_full_name, user_email, user_hashed_password, user_password_salt
        )

        if save_user_response["success"]:
            return ApiResponse.success(
                message="SERVER_REGISTRATION_SUCCESSFUL",
                data={"token": registration_token},
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


    # Hash Passwords
    def hash_user_password(self, user_password):
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user_password.encode("utf-8"), salt)
            return hashed_password.decode("utf-8"), salt.decode("utf-8")
        except Exception as hashing_error:
            raise ApiException.internal_server_error(
                message="SERVER_PASSWORD_HASH_FAILURE", data=str(hashing_error)
            )


    # Save User Registration
    async def save_user_registration(self, user_full_name, user_email, user_hashed_password, user_password_salt):
        try:
            await self.database.execute_stored_procedure(
                Procedures.SAVE_USER_REGISTRATION_SP.value,
                user_full_name,
                user_email,
                user_hashed_password,
                user_password_salt,
            )
            return {"success": True, "data": None}

        except Exception as error:
            if str(error) == "DB_USER_ALREADY_EXISTS":
                raise ApiException.conflict_error(message="SERVER_USER_ALREADY_EXISTS")
            else:
                raise ApiException.internal_server_error(
                    message="SERVER_SAVE_USER_DB_FAILURE", data=str(error)
                )

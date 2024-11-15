import bcrypt
import jwt

from backend.models.users_model import UsersModel
from backend.database.schemas.authentication_schema import ResetPasswordSchema

from backend.services.BaseService import BaseService

from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse

from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError

from backend.utils.logging_utils import *
from backend.enumerations.enums import *
from backend.constants.const import *


class ResetPasswordService(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = ResetPasswordSchema(**request)

    async def handle_request(self):
        # Extract Input Parameters
        password_reset_token = self.request_parameters.token
        new_password = self.request_parameters.user_password

        # Verify Token Validity
        decoded_token = self.verify_token_validity(password_reset_token)
        user_email = decoded_token["user_email"]

        # Hash Password
        user_hashed_password, user_password_salt = self.hash_user_password(new_password)

        # Update User Password in Database
        update_password_response = await self.update_user_password_in_database(
            user_email, user_hashed_password, user_password_salt
        )

        if update_password_response["success"]:
            return ApiResponse.success(
                message="SERVER_PASSWORD_RESET_SUCCESSFUL", data={}
            )

    # Hash Password
    def hash_user_password(self, user_password):
        """
        Hashes the user's password using bcrypt.

        Args:
            user_password (str): The plain text password to be hashed.

        Returns:
            tuple: A tuple containing the hashed password and the salt used for hashing.

        Raises:
            ApiException: If there is an error during the hashing process.
        """
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user_password.encode("utf-8"), salt)
            return hashed_password.decode("utf-8"), salt.decode("utf-8")
        except Exception as hashing_error:
            raise ApiException.internal_server_error(
                message="SERVER_PASSWORD_HASH_FAILURE", data=str(hashing_error)
            )

    # Verify Token Validity
    def verify_token_validity(self, token):
        """
        Verifies the validity of a JWT token.

        Args:
            token (str): The JWT token to be verified.

        Returns:
            dict: The decoded token if it is valid.

        Raises:
            ApiException: If the token is expired or invalid.
        """
        try:
            decoded_token = jwt.decode(token, SECRET_NAME, algorithms=["HS256"])
            expiration = datetime.datetime.fromtimestamp(decoded_token["exp"])
            return decoded_token
        except ExpiredSignatureError:
            raise ApiException.internal_server_error(
                message="SERVER_PASSWORD_RESET_TOKEN_EXPIRED",
            )
        except InvalidTokenError:
            raise ApiException.internal_server_error(
                message="SERVER_PASSWORD_RESET_INVALID_TOKEN",
            )

    # Update User Password in Database
    async def update_user_password_in_database(
        self, user_email, user_hashed_password, user_password_salt
    ):
        """
        Updates the user's password in the database.

        Args:
            user_email (str): The email of the user whose password is being updated.
            user_hashed_password (str): The hashed password to be stored.
            user_password_salt (str): The salt used for hashing the password.

        Returns:
            dict: A dictionary indicating the success of the operation.

        Raises:
            ApiException: If there is an error during the database operation.
        """
        try:
            await self.database.execute_stored_procedure(
                Procedures.SAVE_USER_PASSWORD_SP.value,
                user_email,
                user_hashed_password,
                user_password_salt,
            )
            return {"success": True, "data": None}

        except Exception as error:
            raise ApiException.internal_server_error(
                message="SERVER_RESET_PASSWORD_DB_FAILURE", data=str(error)
            )

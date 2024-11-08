import bcrypt
import jwt

from backend.models.users_model import UsersModel
from backend.utils.logging_utils import *
from backend.services.BaseService import BaseService
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError


class ResetPasswordService(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = request

    def handle_request(self):
        """
        Handles the password reset request by verifying the token and updating the user's password.

        Raises:
            ApiException: If the token is invalid or expired.
        """
        # Extract Input Parameters
        password_reset_token = self.request_parameters.get('token')
        new_password = self.request_parameters.get('userPassword')

        # Verify Token Validity
        decoded_token = self.verify_token_validity(password_reset_token)
        user_email = decoded_token['user_email']

        # Hash Password
        hashed_password, salt = self.hash_user_password(new_password)

        # Update User Password in Database
        self.update_user_password_in_database(user_email, hashed_password, salt)

        return ApiResponse.success(
            message = "SERVER_PASSWORD_RESET_SUCCESSFUL", 
            data = {}
        )


    # Hash Password
    def hash_user_password(self, user_password):
        """
        Hashes the user's password and generates a salt.

        Args:
            user_password (str): The user's new password to be hashed.

        Returns:
            tuple: A tuple containing the hashed password and the salt used.

        Raises:
            ApiException: If there is an error during the hashing process.
        """
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt)
            return hashed_password.decode('utf-8'), salt.decode('utf-8')
        except Exception as hashing_error:
            raise ApiException.internal_server_error(
                message="SERVER_PASSWORD_HASH_FAILURE",
                data=str(hashing_error)
            )

    # Verify Token Validity
    def verify_token_validity(self, token):
        """
        Verifies the validity of the provided password reset token.

        Args:
            token (str): The password reset token to be verified.

        Returns:
            dict: The decoded token if valid.

        Raises:
            ApiException: If the token is expired or invalid.
        """
        try:
            decoded_token = jwt.decode(token, SECRET_NAME, algorithms=["HS256"])
            expiration = datetime.fromtimestamp(decoded_token['exp'])
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
    def update_user_password_in_database(self, user_email, hashed_password, salt):
        """
        Updates the user's password in the database.

        Args:
            user_email (str): The email of the user to be updated.
            hashed_password (str): The hashed password to be updated.
            salt (str): The salt used to hash the password.

        Raises:
            ApiException: If there is an error during the database update.
        """
        dataset = {
            "user_email": user_email,
            "user_password": hashed_password,
            "user_password_salt": salt
        }

        update_user_password = self.prepare_request_parameters(
            event=Events.UPDATE.value,
            table=Tables.TABLE_USERS.value,
            model=UsersModel,
            dataset=dataset
        )
        try:
            result = self.database.database_request(update_user_password)
            return result
        except Exception as error:
            raise ApiException.internal_server_error(
                message="SERVER_DATABASE_UPDATE_FAILURE",
                data=str(error)
            )

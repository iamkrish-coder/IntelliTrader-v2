# Registration

import jwt
import time
import bcrypt

from backend.database.models.users_model import UsersModel
from backend.database.schemas.users_schema import UsersSchema

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
        """
        Handles the user registration request by generating a user ID,
        creating a JWT token, hashing the user's password, preparing
        the dataset for the database, and saving the user to the database.
        
        Returns:
            ApiResponse: A successful response containing the JWT token.
        """
        # Extract Input Parameters
        user_full_name = self.request_parameters.user_full_name
        user_email = self.request_parameters.user_email
        user_password = self.request_parameters.user_password

        # Generate JWT Token
        registration_token = self.generate_jwt_token(user_email)

        # Hash Passwords
        user_hashed_password, user_password_salt = self.hash_user_password(user_password)

        # save user to database
        await self.save_user_to_database(user_full_name, user_email, user_hashed_password, user_password_salt)

        return ApiResponse.success(
            message = "SERVER_REGISTRATION_SUCCESSFUL", 
            data = {"token": registration_token}
        )

    # Generate User ID
    def generate_user_id(self):
        """
        Generates a unique user ID for the new user.
        
        Returns:
            str: A unique user ID.
        """
        return self.generate_table_uid(TABLE_USERS)

    # Generate JWT Token
    def generate_jwt_token(self, user_email):
        """
        Generates a JWT token for the user based on the user ID and email.
        
        Raises:
            ApiException: If user ID or email is not found, invalid, or improperly formatted.
        
        Returns:
            str: The generated JWT token.
        """
        if not user_email:
            raise ApiException.validation_error(
                message = "SERVER_EMAIL_NOT_FOUND"
            )

        if not isinstance(user_email, str):
            raise ApiException.invalid_data_type_error(
                message = "SERVER_INVALID_USER_ID_EMAIL_TYPE"
            )

        if "@" not in user_email:
            raise ApiException.bad_request_error(
                message = "SERVER_INVALID_EMAIL_FORMAT"
            )

        # Create payload
        payload = {
            "userEmail": user_email,
        }

        # Generate JWT Tokens
        try:
            return jwt.encode(payload, SECRET_NAME, algorithm="HS256")
        except jwt.PyJWTError as jwt_error:
            raise ApiException.internal_server_error(
                message = "SERVER_JWT_GENERATION_FAILED", 
                data = str(jwt_error)
            )

    # Hash Passwords
    def hash_user_password(self, user_password):
        """
        Hashes the user's password and generates a salt.
        
        Raises:
            ApiException: If there is an error during the hashing process.
        """
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt)
            return hashed_password.decode('utf-8'), salt.decode('utf-8')
        except Exception as hashing_error:
            raise ApiException.internal_server_error(
                message = "SERVER_PASSWORD_HASH_FAILURE", 
                data = str(hashing_error)
            )

    # Save User to Database
    async def save_user_to_database(self, user_full_name, user_email, user_hashed_password, user_password_salt):
        """
        Saves the user data to the database.
        
        Args:
            dataset (dict): The user data to be saved.
        
        Raises:
            ApiException: If there is an error during the database save operation.
        
        Returns:
            result: The result of the database save operation.
        """
        try:
            result = await self.database.execute_stored_procedure(
                Procedures.SAVE_USER_REGISTRATION_SP.value, 
                user_full_name, 
                user_email, 
                user_hashed_password, 
                user_password_salt, 
            )
            return result
        except Exception as error:
            if str(error) == 'DB_USER_ALREADY_EXISTS':
                raise ApiException.conflict_error(
                    message = "SERVER_USER_ALREADY_EXISTS"
                )
            else:   
                raise ApiException.internal_server_error(
                    message = "SERVER_SAVE_USER_DB_FAILURE", 
                    data = str(error)
                )

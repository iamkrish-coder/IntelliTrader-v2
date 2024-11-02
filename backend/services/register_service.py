# Registration

import jwt
import time
import bcrypt

from backend.utils.logging_utils import *
from backend.models.users_model import UsersModel
from backend.services.BaseService import BaseService
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse


class Register(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = request

    def handle_request(self):
        """
        Handles the user registration request by generating a user ID,
        creating a JWT token, hashing the user's password, preparing
        the dataset for the database, and saving the user to the database.
        
        Returns:
            ApiResponse: A successful response containing the JWT token.
        """
        # Extract Input Parameters
        user_id = self.generate_user_id()
        user_name = self.request_parameters.get('userFullName')
        user_email = self.request_parameters.get('userEmail')
        user_password = self.request_parameters.get('userPassword')

        # Validate Input Parameters
        self.validate_input_parameters(user_name=user_name, user_email=user_email, user_password=user_password)

        # Generate JWT Token
        registration_token = self.generate_jwt_token(user_id, user_email)

        # Hash Passwords
        hashed_password, salt = self.hash_user_password(user_password)

        # save user to database
        self.save_user_to_database(user_id, user_name, user_email, hashed_password, salt)

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

    # Validate Input Parameters
    def validate_input_parameters(self, **kwargs):
        """
        Validates the input parameters to ensure none are missing.
        
        Args:
            **kwargs: Keyword arguments representing user input parameters.
        
        Raises:
            ApiException: If any required parameter is missing.
        """
        required_params = ['user_name', 'user_email', 'user_password']
        for param in required_params:
            if param not in kwargs or not kwargs[param]:
                raise ApiException.validation_error(
                    message = "SERVER_REQUIRED_INFORMATION",
                    data = f"Missing required parameter: {param}"
                )

    # Generate JWT Token
    def generate_jwt_token(self, user_id, user_email):
        """
        Generates a JWT token for the user based on the user ID and email.
        
        Raises:
            ApiException: If user ID or email is not found, invalid, or improperly formatted.
        
        Returns:
            str: The generated JWT token.
        """

        # Validations
        if not user_id:
            raise ApiException.validation_error(
                message = "SERVER_USER_ID_NOT_FOUND"
            )

        if not user_email:
            raise ApiException.validation_error(
                message = "SERVER_EMAIL_NOT_FOUND"
            )

        if not isinstance(user_id, str) or not isinstance(user_email, str):
            raise ApiException.invalid_data_type_error(
                message = "SERVER_INVALID_USER_ID_EMAIL_TYPE"
            )

        if "@" not in user_email:
            raise ApiException.bad_request_error(
                message = "SERVER_INVALID_EMAIL_FORMAT"
            )

        # Create payload
        payload = {
            "userId": user_id,
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
    def save_user_to_database(self, user_id, user_name, user_email, hashed_password, salt):
        """
        Saves the user data to the database.
        
        Args:
            dataset (dict): The user data to be saved.
        
        Raises:
            ApiException: If there is an error during the database save operation.
        
        Returns:
            result: The result of the database save operation.
        """
        dataset = {
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "user_password": hashed_password,
            "user_password_salt": salt,
            "created_date": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        save_user = self.prepare_request_parameters(
            event=Events.PUT.value,
            table=Tables.TABLE_USERS.value,
            model=UsersModel,
            dataset=dataset
        )
        try:
            result = self.database.database_request(save_user)
            return result
        except Exception as error:
            if hasattr(error, 'response'):
                error_code = error.response['Error'].get('Code', None)
                if error_code == 'ConditionalCheckFailedException':
                    raise ApiException.conflict_error(
                        message = "SERVER_USER_ALREADY_EXISTS"
                    )

            raise ApiException.internal_server_error(
                message = "SERVER_SAVE_USER_DB_FAILURE", 
                data = str(error)
            )

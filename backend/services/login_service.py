# Registration
import bcrypt
import jwt

from backend.models.users_model import UsersModel
from backend.utils.logging_utils import *
from backend.services.BaseService import BaseService
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse


class LoginService(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = request

    def handle_request(self):
        """
        Handles the login request by validating input parameters,
        retrieving user credentials, and generating a JWT token if valid.
        """
        # Extract Input Parameters
        user_email  = self.request_parameters.get('userEmail')
        entered_password = self.request_parameters.get('userPassword')

        # Validate Input Parameters
        self.validate_input_parameters(user_email=user_email, entered_password=entered_password)

        # Get User Login Credentials
        stored_password = self.get_user_login_credentials(user_email)

        # Generate JWT Token
        login_token = self.generate_jwt_token(user_email)

        if self.validate_password(stored_password, entered_password):
            return ApiResponse.success(
                message = "SERVER_LOGIN_SUCCESSFUL", 
                data = {"token": login_token}
            )
        else:
            raise ApiException.validation_error(
                message = "SERVER_INVALID_CREDENTIALS"
            )

    # Validate Input Parameters
    def validate_input_parameters(self, **kwargs):
        """
        Validates the input parameters to ensure none are missing.
        
        Args:
            **kwargs: Keyword arguments representing user input parameters.
        
        Raises:
            ApiException: If any required parameter is missing.
        """
        required_params = ['user_email', 'entered_password']
        for param in required_params:
            if param not in kwargs or not kwargs[param]:
                raise ApiException.validation_error(
                    message = "SERVER_REQUIRED_INFORMATION",
                    data = f"Missing required parameter: {param}"
                )

    # Get User Login Credentials
    def get_user_login_credentials(self, user_email):
        """
        Retrieves the stored password for the given user email from the database.
        
        Args:
            user_email (str): The email of the user attempting to log in.
        
        Returns:
            str: The stored password for the user.
        
        Raises:
            ApiException: If the email is incorrect or if there is a database error.
        """
        dataset = {
            "user_email": user_email
        }
        lookup_user_params = self.prepare_request_parameters(
            event=Events.GET.value,
            table=Tables.TABLE_USERS.value,
            model=UsersModel,
            dataset=dataset,
            projection=["user_email, user_password"],
            filters={
                "user_email": { "eq": user_email }
            }
        )

        try:
            fetch_user = self.database_request(lookup_user_params)
            if fetch_user is not None:
                stored_password = self.get_stored_password(fetch_user)
                return stored_password
            else:
                raise ApiException.validation_error(
                    message = "SERVER_LOGIN_EMAIL_INCORRECT"
                )
        except Exception as error:
            raise ApiException.internal_server_error(
                message = "SERVER_GET_USER_DB_FAILURE", 
                data = str(error)
            )

    # Generate JWT Token
    def generate_jwt_token(self, user_email):
        """
        Generates a JWT token for the given user email.
        
        Args:
            user_email (str): The email of the user for whom the token is generated.
        
        Returns:
            str: The generated JWT token.
        
        Raises:
            ApiException: If the user email is not found.
        """
        if not user_email:
            raise ApiException.validation_error(
                message = "SERVER_EMAIL_NOT_FOUND"
            )
        
        payload = { "userEmail": user_email }
        jwt_token = jwt.encode(payload, SECRET_NAME, algorithm="HS256")
        return jwt_token

    # Get Stored Password
    def get_stored_password(self, saved_login_credentials):
        """
        Extracts the stored password from the fetched user credentials.
        
        Args:
            saved_login_credentials (list): The list of user credentials fetched from the database.
        
        Returns:
            str: The stored password of the user.
        """
        return saved_login_credentials['user_password']

    # Validate Password
    def validate_password(self, stored_password, entered_password):
        """
        Validates the entered password against the stored password.
        
        Args:
            stored_password (str): The password stored in the database.
            entered_password (str): The password entered by the user.
        
        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))

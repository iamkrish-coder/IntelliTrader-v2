import jwt

from backend.models.users_model import UsersModel
from backend.utils.logging_utils import *
from backend.services.BaseService import BaseService
from backend.services.email_service import EmailService
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse
from datetime import datetime, timedelta, timezone 


class ForgotPasswordService(BaseService):

    def __init__(self, request):
        super().__init__()
        self.request_parameters = request

    def handle_request(self):
        """
        Handles the forgot password request by validating input, 
        generating a token, saving it, and sending an email with the token.
        """
        # Extract Input Parameters
        user_email = self.request_parameters.get('userEmail')

        # Validate Input Parameters
        self.validate_input_parameters(user_email=user_email)

        # Checks User Existence
        self.get_user_login_credentials(user_email)

        # Generate a secure token
        forgot_password_token = self.generate_forgot_password_token(user_email)
        
        # Save the token 
        self.save_forgot_password_token(user_email, forgot_password_token)

        # Send an email with the token 
        send_email = self.send_forgot_password_email(user_email, forgot_password_token)

        if send_email["success"]:
            return ApiResponse.success(
                message = "SERVER_FORGOT_PASSWORD_EMAIL_SENT", 
                data = {"token": forgot_password_token}
            )
        else:
            raise ApiException.internal_server_error(
                message = "SERVER_FORGOT_PASSWORD_EMAIL_SENDING_FAILURE", 
                data = str(send_email["error"])
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
        required_params = ['user_email']
        for param in required_params:
            if param not in kwargs or not kwargs[param]:
                raise ApiException.validation_error(
                    message = "SERVER_REQUIRED_INFORMATION",
                    data = f"Missing required parameter: {param}"
                )

    # Send Forgot Password Email
    def send_forgot_password_email(self, user_email, forgot_password_token):
        """
        Sends a forgot password email to the user with a reset link containing the token.
        
        Args:
            user_email (str): The email address of the user.
            forgot_password_token (str): The token for password reset.
        
        Returns:
            dict: The result of the email sending operation.
        """
        email_object = EmailService()
        send_email = email_object.send_email(
            recipient_email = user_email, 
            template = "forgot_password", 
            reset_link = f"http://localhost:5173/reset-password/token={forgot_password_token}"
        )
        return send_email

    # Save Forgot Password Token
    def save_forgot_password_token(self, user_email, forgot_password_token):     
        """
        Saves the generated forgot password token associated with the user's email.
        
        Args:
            user_email (str): The email address of the user.
            forgot_password_token (str): The token for password reset.
        
        Returns:
            Any: The result of the database save operation.
        
        Raises:
            ApiException: If there is an error saving the token.
        """
        dataset = { 
            "user_email": user_email,
            "user_password_reset_token": forgot_password_token,
        }
        update_topics = self.prepare_request_parameters(
            event=Events.UPDATE.value,
            table=Tables.TABLE_USERS.value,
            model=UsersModel,
            dataset=dataset
        )

        try:
            save_token = self.database.database_request(update_topics)
            return save_token
        except Exception as error:
            raise ApiException.internal_server_error(
                message = "SERVER_FORGOT_PASSWORD_TOKEN_SAVING_FAILURE", 
                data = str(error)
            )

    # Generate Forgot Password Token
    def generate_forgot_password_token(self, user_email):
        """
        Generates a JWT token for password reset with an expiration time.
        
        Args:
            user_email (str): The email address of the user.
        
        Returns:
            str: The generated JWT token.
        
        Raises:
            ApiException: If there is an error generating the token.
        """
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=15)  # Token expires in 15 minutes
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

    # Get User Login Credentials
    def get_user_login_credentials(self, user_email):
        """
        Retrieves the user's login credentials based on the provided email.
        
        Args:
            user_email (str): The email address of the user.
        
        Returns:
            Any: The user's login credentials.
        
        Raises:
            ApiException: If the user is not found or there is a database error.
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
            if not fetch_user:
                raise ApiException.validation_error(
                    message = "SERVER_FORGOT_PASSWORD_EMAIL_INCORRECT"
                )
            else:
                return fetch_user
        except Exception as error:
            raise ApiException.internal_server_error(
                message = "SERVER_GET_USER_DB_FAILURE", 
                data = str(error)
            )

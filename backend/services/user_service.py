import jwt
import time
import bcrypt

from backend.utils.logging_utils import *
from backend.enumerations.enums import *
from backend.constants.const import *

from typing import Dict, Any
from backend.database.managers.database_manager import DatabaseManager
from backend.database.repositories.user_repository import UserRepository
from backend.domain.models.users import Users
from backend.schemas.schema import UserSchema
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse

class UserService:
    def __init__(self, db_manager, request_data: Dict[str, Any]):
        self.user_repository = UserRepository(db_manager)
        self.request_parameters = UserSchema(**request_data)

    async def handle_request(self) -> ApiResponse:
        """
        Handle OAuth user registration/login request.
        
        Returns:
            ApiResponse with operation result
        """
        try:
            # Create domain model from validated OAuth data
            user_model_data = Users.from_oauth(
                email=self.request_parameters.email,
                name=self.request_parameters.name,
                picture=self.request_parameters.picture,
                provider_id=self.request_parameters.provider_id,
                oauth_provider=self.request_parameters.oauth_provider
            )

            # Check if user exists
            existing_user = await self.user_repository.get_user_by_email(user_model_data.email)
            
            if existing_user.get("status") == 0:
                # Save new user account
                save_result = await self.user_repository.create_user(user_model_data)
                if not save_result["success"]:
                    raise ApiException.internal_server_error(
                        message="Failed to create account"
                    )
                return ApiResponse(
                    message="Account created successfully",
                    data=None
                )
            else:
                return ApiResponse(
                    message="Account already exists",
                    data=None
                )             
        except Exception as e:
            log_error(f"OAuth request processing error: {str(e)}")
            raise ApiException.internal_server_error(
                message="OAuth request processing failed",
                data=str(e)
            )

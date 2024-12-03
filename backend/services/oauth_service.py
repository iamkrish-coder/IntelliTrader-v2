import jwt
import time
import bcrypt

from backend.utils.logging_utils import *
from backend.enumerations.enums import *
from backend.constants.const import *

from typing import Dict, Any
from backend.repositories.user_repository import UserRepository
from backend.domain.models.user import User
from backend.schemas.oauth_schema import OAuthUserSchema
from backend.database.database_manager import DatabaseManager
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse

class OAuthService:
    def __init__(self, db: DatabaseManager, request_data: Dict[str, Any]):
        self.user_repository = UserRepository(db)
        self.request_parameters = OAuthUserSchema(**request_data)

    async def handle_request(self) -> ApiResponse:
        """
        Handle OAuth user registration/login request.
        
        Returns:
            ApiResponse with operation result
        """
        try:
            # Create domain model from validated OAuth data
            user = User.from_oauth(
                email=self.request_parameters.email,
                name=self.request_parameters.name,
                picture=self.request_parameters.picture,
                provider_id=self.request_parameters.provider_id,
                oauth_provider=self.request_parameters.oauth_provider
            )

            # Check if user exists
            existing_user = await self.user_repository.get_user_by_email(user.email)
            
            if not existing_user:
                # Save new user
                save_result = await self.user_repository.save_oauth_user(user)
                if not save_result["success"]:
                    raise ApiException.internal_server_error(
                        message="Failed to save OAuth user"
                    )

            return ApiResponse(
                message="OAuth user processed successfully",
                data=user.to_dict()
            )
        except Exception as e:
            log_error(f"OAuth request processing error: {str(e)}")
            raise ApiException.internal_server_error(
                message="OAuth request processing failed",
                data=str(e)
            )

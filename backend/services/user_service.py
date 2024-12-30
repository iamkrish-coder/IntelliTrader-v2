from datetime import datetime
import time
from typing import Dict, Any

from backend.utils.logging_utils import *
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse
from backend.domain.schemas.user_schema import UserSchema
from backend.domain.models.user_model import UserModel
from backend.domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db_manager, request_data: Dict[str, Any]):
        self.user_repository = UserRepository(db_manager)
        self.request_parameters = request_data

    async def create_new_user_account(self) -> ApiResponse:
        """Create a new user account."""
        try:
            # Validate request data
            user_schema = UserSchema(**self.request_parameters)
            
            # Create domain model from validated data
            user = UserModel(
                email=user_schema.email,
                name=user_schema.name,
                image=user_schema.image,
                emailVerified=datetime.utcnow() if user_schema.emailVerified else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Check if user exists
            existing_user = await self.user_repository.get_user_by_email(user.email)
            
            if existing_user.get("status") == 0:
                # Save new user account
                save_result = await self.user_repository.create_user_account(user)
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
            log_error(f"Create user error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to create user",
                data=str(e)
            )

    async def get_user_by_id(self) -> ApiResponse:
        """Get a user by their ID."""
        try:
            user_id = self.request_parameters.get("id")
            if not user_id:
                raise ApiException.bad_request(message="User ID is required")
            
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise ApiException.not_found(message="User not found")
                
            return ApiResponse(
                message="User retrieved successfully",
                data=user
            )
        except Exception as e:
            log_error(f"Get user by ID error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to retrieve user",
                data=str(e)
            )

    async def get_user_by_email(self) -> ApiResponse:
        """Get a user by their email address."""
        try:
            email = self.request_parameters.get("email")
            if not email:
                raise ApiException.bad_request(message="Email is required")
            
            user = await self.user_repository.get_user_by_email(email)
            if not user:
                raise ApiException.not_found(message="User not found")
                
            return ApiResponse(
                message="User retrieved successfully",
                data=user
            )
        except Exception as e:
            log_error(f"Get user by email error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to retrieve user",
                data=str(e)
            )

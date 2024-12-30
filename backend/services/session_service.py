from datetime import datetime
import time
from typing import Dict, Any

from backend.utils.logging_utils import *
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse
from backend.domain.schemas.session_schema import SessionSchema
from backend.domain.models.session_model import SessionModel
from backend.domain.repositories.session_repository import SessionRepository

class SessionService:
    def __init__(self, db_manager, request_data: Dict[str, Any]):
        self.session_repository = SessionRepository(db_manager)
        self.request_parameters = request_data

    async def create_session(self) -> ApiResponse:
        """Create a new user session."""
        try:
            session_schema = SessionSchema(**self.request_parameters)
            
            session = SessionModel(
                id=str(time.time_ns()),
                sessionToken=session_schema.sessionToken,
                userId=session_schema.userId,
                expires=session_schema.expires,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            result = await self.session_repository.create_session(session)
            if not result["success"]:
                raise ApiException.internal_server_error(
                    message="Failed to create session"
                )
                
            return ApiResponse(
                message="Session created successfully",
                data=session.to_dict()
            )
        except Exception as e:
            log_error(f"Create session error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to create session",
                data=str(e)
            )

    async def get_session_and_user(self) -> ApiResponse:
        """Get a session and its associated user."""
        try:
            session_token = self.request_parameters.get("sessionToken")
            if not session_token:
                raise ApiException.bad_request(message="Session token is required")
            
            result = await self.session_repository.get_session_and_user(session_token)
            if not result:
                raise ApiException.not_found(message="Session not found")
                
            return ApiResponse(
                message="Session and user retrieved successfully",
                data=result
            )
        except Exception as e:
            log_error(f"Get session and user error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to retrieve session and user",
                data=str(e)
            )

    async def update_session(self, session_token: str) -> ApiResponse:
        """Update an existing session."""
        try:
            session_schema = SessionSchema(**self.request_parameters)
            
            session = SessionModel(
                sessionToken=session_token,
                expires=session_schema.expires,
                updated_at=datetime.utcnow()
            )
            
            result = await self.session_repository.update_session(session)
            if not result["success"]:
                raise ApiException.not_found(message="Session not found")
                
            return ApiResponse(
                message="Session updated successfully",
                data=session.to_dict()
            )
        except Exception as e:
            log_error(f"Update session error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to update session",
                data=str(e)
            )

    async def delete_session(self) -> ApiResponse:
        """Delete a session."""
        try:
            session_token = self.request_parameters.get("sessionToken")
            if not session_token:
                raise ApiException.bad_request(message="Session token is required")
            
            result = await self.session_repository.delete_session(session_token)
            if not result["success"]:
                raise ApiException.not_found(message="Session not found")
                
            return ApiResponse(
                message="Session deleted successfully"
            )
        except Exception as e:
            log_error(f"Delete session error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to delete session",
                data=str(e)
            )

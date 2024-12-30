from datetime import datetime
from typing import Dict, Any

from backend.utils.logging_utils import *
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse
from backend.domain.schemas.verification_token_schema import VerificationTokenSchema
from backend.domain.models.verification_token_model import VerificationTokenModel
from backend.domain.repositories.verification_token_repository import VerificationTokenRepository

class VerificationTokenService:
    def __init__(self, db_manager, request_data: Dict[str, Any]):
        self.token_repository = VerificationTokenRepository(db_manager)
        self.request_parameters = request_data

    async def create_verification_token(self) -> ApiResponse:
        """Create a new verification token."""
        try:
            token_schema = VerificationTokenSchema(**self.request_parameters)
            
            token = VerificationTokenModel(
                identifier=token_schema.identifier,
                token=token_schema.token,
                expires=token_schema.expires,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            result = await self.token_repository.create_verification_token(token)
            if not result["success"]:
                raise ApiException.internal_server_error(
                    message="Failed to create verification token"
                )
                
            return ApiResponse(
                message="Verification token created successfully",
                data=token.to_dict()
            )
        except Exception as e:
            log_error(f"Create verification token error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to create verification token",
                data=str(e)
            )

    async def use_verification_token(self) -> ApiResponse:
        """Use and delete a verification token."""
        try:
            identifier = self.request_parameters.get("identifier")
            token = self.request_parameters.get("token")
            
            if not identifier or not token:
                raise ApiException.bad_request(
                    message="Identifier and token are required"
                )
            
            result = await self.token_repository.use_verification_token(identifier, token)
            if not result["success"]:
                raise ApiException.not_found(message="Verification token not found")
                
            return ApiResponse(
                message="Verification token used successfully",
                data=result["data"]
            )
        except Exception as e:
            log_error(f"Use verification token error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to use verification token",
                data=str(e)
            )

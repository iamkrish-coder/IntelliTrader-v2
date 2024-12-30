from datetime import datetime
import time
from typing import Dict, Any

from backend.utils.logging_utils import *
from backend.core.exceptions import ApiException
from backend.core.response import ApiResponse
from backend.domain.schemas.account_schema import AccountSchema
from backend.domain.models.account_model import AccountModel
from backend.domain.repositories.account_repository import AccountRepository

class AccountService:
    def __init__(self, db_manager, request_data: Dict[str, Any]):
        self.account_repository = AccountRepository(db_manager)
        self.request_parameters = request_data

    async def link_account(self) -> ApiResponse:
        """Link an OAuth account to a user."""
        try:
            account_schema = AccountSchema(**self.request_parameters)
            
            account = AccountModel(
                id=str(time.time_ns()),
                userId=account_schema.userId,
                type=account_schema.type,
                provider=account_schema.provider,
                providerAccountId=account_schema.providerAccountId,
                refresh_token=account_schema.refresh_token,
                access_token=account_schema.access_token,
                expires_at=account_schema.expires_at,
                token_type=account_schema.token_type,
                scope=account_schema.scope,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            result = await self.account_repository.link_account(account)
            if not result["success"]:
                raise ApiException.internal_server_error(
                    message="Failed to link account"
                )
                
            return ApiResponse(
                message="Account linked successfully",
                data=account.to_dict()
            )
        except Exception as e:
            log_error(f"Link account error: {str(e)}")
            raise ApiException.internal_server_error(
                message="Failed to link account",
                data=str(e)
            )

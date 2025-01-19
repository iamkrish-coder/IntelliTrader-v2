from typing import Dict, Any
from backend.domain.repositories.base_repository import BaseRepository
from backend.database.managers.database_manager import DatabaseManager
from backend.domain.models.user_model import UserModel
from backend.enumerations.enums import Procedures, Functions

class UserRepository(BaseRepository):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    async def create_user_account(self, user: UserModel) -> Dict[str, Any]:
        """Create a new user account."""
        return await self.execute_procedure(
            Procedures.CREATE_USER_ACCOUNT_SP.value,
            user.name,
            user.email,
            user.emailVerified,
            user.image
        )

    async def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """Get a user by their ID."""
        return await self.execute_procedure(
            Procedures.GET_USER_BY_ID_SP.value,
            user_id
        )

    async def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """Get a user by their email."""
        return await self.execute_function(
            Functions.GET_USER_BY_EMAIL_FN.value,
            email
        )

    async def get_user_by_account(self, provider: str, provider_account_id: str):
        """Get a user by their account provider and ID."""
        return await self.execute_function(
            Functions.GET_USER_BY_ACCOUNT_FN.value,
            provider,
            provider_account_id
        )


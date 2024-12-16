from typing import Optional, Dict, List, Any
from backend.database.repositories.base_repository import BaseRepository
from backend.database.managers.database_manager import DatabaseManager
from backend.domain.models.users import Users
from backend.enumerations.enums import Procedures, Functions

import asyncpg

class UserRepository(BaseRepository):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    async def create_user(self, user: Users) -> Dict[str, Any]:
        return await self.execute_procedure(
            Procedures.CREATE_USER_ACCOUNT_SP.value,
            user.name,
            user.email,
            user.picture,
            user.provider_id,
            user.oauth_provider,
            None,  # No password for OAuth users
            None,   # No salt for OAuth users,
            transaction=True
        )

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        result = await self.execute_function(
            Functions.GET_USER_BY_EMAIL_FN.value,
            email,
            fetch_mode='one'
        )
        return result.get('data') if result['success'] else None

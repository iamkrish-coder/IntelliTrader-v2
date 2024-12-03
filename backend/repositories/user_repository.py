from typing import Dict, Optional, Any
from backend.repositories.base_repository import BaseRepository
from backend.database.database_manager import DatabaseManager
from backend.domain.models.user import User
from backend.enumerations.enums import Procedures

class UserRepository(BaseRepository):
    def __init__(self, db: DatabaseManager):
        super().__init__(db)

    async def save_oauth_user(self, user: User) -> Dict[str, Any]:
        """
        Save OAuth user using stored procedure.
        
        Args:
            user: Domain user model
            
        Returns:
            Dict containing the operation result
        """
        return await self.execute_stored_procedure(
            Procedures.SAVE_USER_REGISTRATION_SP.value,
            user.name,
            user.email,
            user.picture,
            user.provider_id,
            user.oauth_provider,
            None,  # No password for OAuth users
            None   # No salt for OAuth users
        )

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email using stored procedure.
        
        Args:
            email: User's email address
            
        Returns:
            Optional[Dict] containing user information if found
        """
        result = await self.execute_stored_procedure(
            Procedures.GET_USER_BY_EMAIL_SP.value,
            email
        )
        return result.get("data")

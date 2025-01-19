from typing import Dict, Any
from backend.domain.repositories.base_repository import BaseRepository
from backend.database.managers.database_manager import DatabaseManager
from backend.domain.models.session_model import SessionModel
from backend.enumerations.enums import Procedures

class SessionRepository(BaseRepository):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    async def create_session(self, session: SessionModel) -> Dict[str, Any]:
        """Create a new session."""
        return await self.execute_procedure(
            Procedures.CREATE_SESSION_SP.value,
            session.sessionToken,
            session.userId,
            session.expires,
            False,
            None
        )

    async def get_session_and_user(self, session_token: str) -> Dict[str, Any]:
        """Get a session and its associated user."""
        return await self.execute_procedure(
            Procedures.GET_SESSION_AND_USER_SP.value,
            session_token
        )

    async def update_session(self, session: SessionModel) -> Dict[str, Any]:
        """Update a session."""
        return await self.execute_procedure(
            Procedures.UPDATE_SESSION_SP.value,
            session.sessionToken,
            session.expires
        )

    async def delete_session(self, session_token: str) -> Dict[str, Any]:
        """Delete a session."""
        return await self.execute_procedure(
            Procedures.DELETE_SESSION_SP.value,
            session_token
        )

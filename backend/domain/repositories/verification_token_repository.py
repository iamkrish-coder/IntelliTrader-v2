from typing import Dict, Any
from backend.domain.repositories.base_repository import BaseRepository
from backend.database.managers.database_manager import DatabaseManager
from backend.domain.models.verification_token_model import VerificationTokenModel
from backend.enumerations.enums import Procedures

class VerificationTokenRepository(BaseRepository):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    async def create_verification_token(self, token: VerificationTokenModel) -> Dict[str, Any]:
        """Create a new verification token."""
        return await self.execute_procedure(
            Procedures.CREATE_VERIFICATION_TOKEN_SP.value,
            token.identifier,
            token.token,
            token.expires
        )

    async def use_verification_token(self, identifier: str, token: str) -> Dict[str, Any]:
        """Use and delete a verification token."""
        return await self.execute_procedure(
            Procedures.USE_VERIFICATION_TOKEN_SP.value,
            identifier,
            token
        )

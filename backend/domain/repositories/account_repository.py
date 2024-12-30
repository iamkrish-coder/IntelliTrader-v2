from typing import Dict, Any
from backend.domain.repositories.base_repository import BaseRepository
from backend.database.managers.database_manager import DatabaseManager
from backend.domain.models.account_model import AccountModel
from backend.enumerations.enums import Procedures

class AccountRepository(BaseRepository):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    async def link_account(self, account: AccountModel) -> Dict[str, Any]:
        """Link an OAuth account to a user."""
        return await self.execute_procedure(
            Procedures.LINK_ACCOUNT_SP.value,
            account.userId,
            account.type,
            account.provider,
            account.providerAccountId,
            account.refresh_token,
            account.access_token,
            account.expires_at,
            account.token_type,
            account.scope,
            account.id_token,
            account.session_state
        )

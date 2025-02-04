from typing import Dict, Any
from backend.domain.repositories.base_repository import BaseRepository
from backend.database.managers.database_manager import DatabaseManager
from backend.domain.models.preferences_model import PreferencesModel
from backend.enumerations.enums import Procedures, Functions

class PreferencesRepository(BaseRepository):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)
    
    async def save_preferences(self, preferences: PreferencesModel) -> Dict[str, Any]:
        """Save user preferences."""
        return await self.execute_procedure(
            Procedures.SAVE_PREFERENCES_SP.value,
            preferences.user_id,
            preferences.debugger_mode,
            preferences.log_level,
            preferences.reset_app,
            preferences.prettier_print,
            preferences.live_trade,
            preferences.topic_type,
            preferences.queue_type,
            preferences.strategy,
            preferences.historical_data_subscription,
            preferences.global_trade,
            preferences.runtime_interval,
            preferences.notify_trades,
            preferences.notify_trades_email,
            preferences.notify_trades_push,
            preferences.notify_price_alerts,
            preferences.notify_price_alerts_email,
            preferences.notify_price_alerts_push,
            preferences.notify_portfolio,
            preferences.notify_portfolio_email,
            preferences.notify_portfolio_push,
            preferences.secret_name,
            preferences.region_name,
            preferences.updated_by
        )

    async def get_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences."""
        return await self.execute_function(
            Functions.GET_PREFERENCES_FN.value,
            user_id,
            fetch_mode='one'
        )
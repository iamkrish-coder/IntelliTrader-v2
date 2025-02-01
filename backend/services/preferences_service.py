from datetime import datetime
import time
from typing import Dict, Any

from backend.utils.logging_utils import log_error
from backend.core.exceptions import ApiException
from backend.domain.schemas.preferences_schema import PreferencesSchema
from backend.domain.models.preferences_model import PreferencesModel
from backend.domain.repositories.preferences_repository import PreferencesRepository

class PreferencesService:
    def __init__(self, db_manager, request_data: Dict[str, Any]):
        self.preferences_repository = PreferencesRepository(db_manager)
        self.request_parameters = request_data
    
    async def save_preferences(self) -> Dict[str, Any]:
        """Save user preferences with streamlined error handling."""
        # Validate request data and create domain model
        try:
            preferences_schema = PreferencesSchema(**self.request_parameters)
        except ValueError as e:
            raise ApiException.validation_error(
                message="Invalid preferences data",
                data={"fields": str(e)}
            )

        # Create domain model
        preferences = PreferencesModel(
            user_id=preferences_schema.user_id,
            debugger_mode=preferences_schema.debugger_mode,
            log_level=preferences_schema.log_level,
            reset_app=preferences_schema.reset_app,
            prettier_print=preferences_schema.prettier_print,
            live_trade=preferences_schema.live_trade,
            topic_type=preferences_schema.topic_type,
            queue_type=preferences_schema.queue_type,
            strategy=preferences_schema.strategy,
            historical_data_subscription=preferences_schema.historical_data_subscription,
            global_trade=preferences_schema.global_trade,
            runtime_interval=preferences_schema.runtime_interval,
            secret_name=preferences_schema.secret_name,
            region_name=preferences_schema.region_name,
            updated_by=preferences_schema.user_id  
        )

        # Save preferences to database
        save_result = await self.preferences_repository.save_preferences(preferences=preferences)
        
        # Handle database operation result
        if not save_result["success"]:
            raise ApiException.database_error(
                message=save_result.get("message", "Failed to save preferences"),
                data=save_result.get("data")
            )
        
        # Return successful response
        return {
            "message": "Preferences saved successfully",
            "data": save_result["data"]
        }

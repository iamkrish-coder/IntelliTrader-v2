from fastapi import APIRouter, Depends, Request
from typing import Optional, List, Dict, Any
from backend.domain.schemas.preferences_schema import PreferencesSchema
from backend.services.preferences_service import PreferencesService
from backend.utils.logging_utils import *
from backend.database.managers.database_manager import DatabaseManager

router = APIRouter()

# Developer Note:
# route -> schema -> service -> model -> repository -> stored procedure/function
# When creating a new route, please refer to the other routes in this file for consistency
# We should have a definition of table created as {table_name}.sql (/backend/database/definitions)
# We should have a schema (/backend/domain/schemas) for the request and response
# We should have a service (/backend/services) for the request and response
# We should have a model (/backend/domain/models) for the building the domain model
# We should have a repository (/backend/domain/repositories) for to call Stored Procedure (/backend/database/stored_procedures) or Function (/backend/database/functions)
# We should have a Stored Procedure (/backend/database/stored_procedures) or Function (/backend/database/functions) created for the database operations

# Preferences Route
@router.post("/settings/preferences")
async def save_preferences(preferences: PreferencesSchema) -> Dict[str, Any]:
    """Save user preferences."""
    db_manager = DatabaseManager.get_instance()
    preferences_service = PreferencesService(db_manager, preferences.model_dump())
    return await preferences_service.save_preferences()

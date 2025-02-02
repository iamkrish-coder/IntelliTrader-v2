from fastapi import APIRouter, Depends, Request
from typing import Optional, List, Dict, Any
from backend.domain.schemas.preferences_schema import PreferencesSchema
from backend.services.preferences_service import PreferencesService
from backend.utils.logging_utils import *
from backend.database.managers.database_manager import DatabaseManager

router = APIRouter()

# Preferences Route
@router.post("/settings/preferences")
async def save_preferences(preferences: PreferencesSchema) -> Dict[str, Any]:
    """Save user preferences."""
    db_manager = DatabaseManager.get_instance()
    preferences_service = PreferencesService(db_manager, preferences.model_dump())
    return await preferences_service.save_preferences()

@router.get("/settings/preferences/{user_id}")
async def get_preferences(user_id: str) -> Dict[str, Any]:
    """Get user preferences."""
    db_manager = DatabaseManager.get_instance()
    preferences_service = PreferencesService(db_manager, user_id)
    return await preferences_service.get_preferences(user_id)
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .user_schema import UserSchema

class AccountSchema(BaseModel):
    """Schema for Account entity."""
    id: Optional[str] = None
    userId: str
    type: str
    provider: str
    providerAccountId: str
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    expires_at: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    session_state: Optional[str] = None
    user: Optional[UserSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

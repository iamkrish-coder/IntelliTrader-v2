from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .user_schema import UserSchema

class SessionSchema(BaseModel):
    """Schema for Session entity."""
    id: Optional[str] = None
    sessionToken: str
    userId: str
    expires: datetime
    user: Optional[UserSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class SessionAndUserSchema(BaseModel):
    """Schema for combined Session and User data."""
    session: SessionSchema
    user: UserSchema

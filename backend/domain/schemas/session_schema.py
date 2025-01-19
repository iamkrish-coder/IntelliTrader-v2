from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .user_schema import UserSchema

class SessionSchema(BaseModel):
    """Schema for Session entity."""
    id: Optional[str] = None
    sessionToken: str
    userId: str = "Srikrishnan"
    expires: datetime
    user: Optional[UserSchema] = None

class SessionAndUserSchema(BaseModel):
    """Schema for combined Session and User data."""
    session: SessionSchema
    user: UserSchema

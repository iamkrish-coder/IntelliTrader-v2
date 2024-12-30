from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserSchema(BaseModel):
    """Schema for User entity."""
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    emailVerified: Optional[datetime] = None
    image: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

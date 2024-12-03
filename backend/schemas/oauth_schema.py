from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class OAuthUserSchema(BaseModel):
    """Schema for validating OAuth user data from frontend"""
    id: Optional[int] = None
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None
    provider_id: Optional[str] = None
    oauth_provider: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

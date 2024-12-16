from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from datetime import datetime

class BaseSchema(BaseModel):
    """Base schema with common fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class StoredProcedureResponse(BaseModel):
    """Schema for stored procedure response data"""
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Any] = None

class UserSchema(BaseSchema):
    """Schema for validating OAuth user data"""
    id: Optional[int] = None
    email: EmailStr
    name: Optional[str] = Field(min_length=2, max_length=100)
    picture: Optional[str] = None
    provider_id: Optional[str] = None
    oauth_provider: Optional[str] = Field(pattern="^(google|github)$")

# Add future schemas here with proper inheritance from BaseSchema where appropriate

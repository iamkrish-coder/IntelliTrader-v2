from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class VerificationTokenSchema(BaseModel):
    """Schema for Verification Token entity."""
    identifier: str
    token: str
    expires: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UseVerificationTokenSchema(BaseModel):
    """Schema for using a verification token."""
    identifier: str
    token: str

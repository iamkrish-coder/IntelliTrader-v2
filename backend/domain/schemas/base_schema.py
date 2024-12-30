from typing import Optional, Dict
from pydantic import BaseModel

class BaseResponse(BaseModel):
    """Base response schema for stored procedures."""
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Dict] = None

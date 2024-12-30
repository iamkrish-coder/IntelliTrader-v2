from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from .users import User

@dataclass
class SessionModel:
    """Domain model for Session entity."""
    id: str
    sessionToken: str
    userId: str
    expires: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[User] = None

    def to_dict(self) -> dict:
        """Convert Session instance to dictionary."""
        return {
            "id": self.id,
            "sessionToken": self.sessionToken,
            "userId": self.userId,
            "expires": self.expires.isoformat(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from .user_model import UserModel

@dataclass
class SessionModel:
    """Domain model for Session entity."""
    id: str
    sessionToken: str
    userId: str
    expires: datetime
    user: Optional[UserModel] = None

    def to_dict(self) -> dict:
        """Convert Session instance to dictionary."""
        return {
            "id": self.id,
            "sessionToken": self.sessionToken,
            "userId": self.userId,
            "expires": self.expires.isoformat(),
        }

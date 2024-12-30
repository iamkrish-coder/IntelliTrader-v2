from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VerificationTokenModel:
    """Domain model for Verification Token entity."""
    identifier: str
    token: str
    expires: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert VerificationToken instance to dictionary."""
        return {
            "identifier": self.identifier,
            "token": self.token,
            "expires": self.expires.isoformat(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

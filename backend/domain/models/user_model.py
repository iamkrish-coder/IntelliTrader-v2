from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class UserModel:
    """Domain model for User entity."""
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    emailVerified: Optional[datetime] = None
    image: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    accounts: List["Account"] = field(default_factory=list)
    sessions: List["Session"] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert User instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "emailVerified": self.emailVerified.isoformat() if self.emailVerified else None,
            "image": self.image,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

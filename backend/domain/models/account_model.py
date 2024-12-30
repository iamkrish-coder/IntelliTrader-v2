from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from .user_model import UserModel

@dataclass
class AccountModel:
    """Domain model for Account entity (OAuth)."""
    id: str
    userId: str
    type: str
    provider: str
    providerAccountId: str
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    expires_at: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    session_state: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[UserModel] = None

    def to_dict(self) -> dict:
        """Convert Account instance to dictionary."""
        return {
            "id": self.id,
            "userId": self.userId,
            "type": self.type,
            "provider": self.provider,
            "providerAccountId": self.providerAccountId,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "expires_at": self.expires_at,
            "token_type": self.token_type,
            "scope": self.scope,
            "id_token": self.id_token,
            "session_state": self.session_state,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

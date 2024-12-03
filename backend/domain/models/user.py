from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """Domain model for User entity."""
    id: Optional[int] = None
    email: str = ""
    name: Optional[str] = None
    picture: Optional[str] = None
    provider_id: Optional[str] = None
    oauth_provider: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_oauth(cls, email: str, name: Optional[str] = None, 
                   picture: Optional[str] = None, 
                   provider_id: Optional[str] = None, 
                   oauth_provider: Optional[str] = None) -> "User":
        """
        Create a User instance from OAuth data.
        
        Args:
            email: User's email from OAuth provider
            name: User's name from OAuth provider
            picture: User's profile picture URL
            provider_id: Unique ID from OAuth provider
            oauth_provider: Name of the OAuth provider
            
        Returns:
            User instance with OAuth data
        """
        return cls(
            email=email,
            name=name,
            picture=picture,
            provider_id=provider_id,
            oauth_provider=oauth_provider,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def to_dict(self) -> dict:
        """Convert User instance to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "picture": self.picture,
            "provider_id": self.provider_id,
            "oauth_provider": self.oauth_provider,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PreferencesModel:
    """Domain model for Preferences entity."""
    id: Optional[int] = None
    user_id: Optional[str] = None
    
    # General Settings
    debugger_mode: bool = False
    log_level: str = "DEBUG"
    reset_app: bool = False
    prettier_print: bool = False
    
    # Trade Settings
    live_trade: bool = False
    topic_type: str = "FIFO"
    queue_type: str = "FIFO"
    strategy: str = "001"
    historical_data_subscription: bool = True
    global_trade: bool = True
    runtime_interval: str = "5MINUTE"
    
    # System Settings
    secret_name: str = "IntelliTrader"
    region_name: str = "ap-south-1"
    
    # Audit Fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    is_active: bool = True

    def to_dict(self) -> dict:
        """Convert Preferences instance to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "debugger_mode": self.debugger_mode,
            "log_level": self.log_level,
            "reset_app": self.reset_app,
            "prettier_print": self.prettier_print,
            "live_trade": self.live_trade,
            "topic_type": self.topic_type,
            "queue_type": self.queue_type,
            "strategy": self.strategy,
            "historical_data_subscription": self.historical_data_subscription,
            "global_trade": self.global_trade,
            "runtime_interval": self.runtime_interval,
            "secret_name": self.secret_name,
            "region_name": self.region_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "is_active": self.is_active
        }

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class PreferencesSchema(BaseModel):
    """Schema for Preferences entity."""
    id: Optional[int] = None
    user_id: Optional[str] = None
    
    # General Settings
    debugger_mode: bool = Field(default=False)
    log_level: str = Field(default="DEBUG")
    reset_app: bool = Field(default=False)
    prettier_print: bool = Field(default=False)
    
    # Trade Settings
    live_trade: bool = Field(default=False)
    topic_type: str = Field(default="FIFO")
    queue_type: str = Field(default="FIFO")
    strategy: str = Field(default="001")
    historical_data_subscription: bool = Field(default=True)
    global_trade: bool = Field(default=True)
    runtime_interval: str = Field(default="5MINUTE")
    
    # Notification Settings
    notify_trades: bool = Field(default=False)
    notify_trades_email: bool = Field(default=False)
    notify_trades_push: bool = Field(default=False)
    notify_price_alerts: bool = Field(default=False)
    notify_price_alerts_email: bool = Field(default=False)
    notify_price_alerts_push: bool = Field(default=False)
    notify_portfolio: bool = Field(default=False)
    notify_portfolio_email: bool = Field(default=False)
    notify_portfolio_push: bool = Field(default=False)
    
    # System Settings
    secret_name: str = Field(default="IntelliTrader")
    region_name: str = Field(default="ap-south-1")
    
    # Audit Fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    is_active: bool = Field(default=True)

    class Config:
        from_attributes = True

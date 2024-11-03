# backend/models/signals_model.py

from backend.models.BaseModel import BaseModel


class SignalsModel(BaseModel):
    def __init__(
        self,
        signal_id=None,
        signal_type=None,
        signal_strategy=None,
        signal_exchange=None,
        signal_symbol=None,
        signal_token=None,
        is_active=None,
        is_complete=None,
        created_date=None
    ):
        super().__init__()

        self.signal_id = signal_id
        self.signal_type = signal_type
        self.signal_strategy = signal_strategy
        self.signal_exchange = signal_exchange
        self.signal_symbol = signal_symbol
        self.signal_token = signal_token
        self.is_active = is_active
        self.is_complete = is_complete
        self.created_date = created_date

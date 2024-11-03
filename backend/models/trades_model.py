# backend/models/trades_model.py

from backend.models.BaseModel import BaseModel


class TradesModel(BaseModel):
    def __init__(
        self,
        trade_id=None,
        trade_signal_id=None,
        trade_strategy=None,
        trade_order_id=None,
        trade_symbol=None,
        trade_entry_time=None,
        trade_entry_price=None,
        trade_position_size=None,
        trade_exit_time=None,
        trade_exit_price=None,
        trade_status=None,
        created_date=None,
        modified_date=None
    ):
        super().__init__()

        self.trade_id = trade_id
        self.trade_signal_id = trade_signal_id
        self.trade_strategy = trade_strategy
        self.trade_order_id = trade_order_id
        self.trade_symbol = trade_symbol
        self.trade_entry_time = trade_entry_time
        self.trade_entry_price = trade_entry_price
        self.trade_position_size = trade_position_size
        self.trade_exit_time = trade_exit_time
        self.trade_exit_price = trade_exit_price
        self.trade_status = trade_status
        self.created_date = created_date
        self.modified_date = modified_date


# IntelliTrader\backend\modules\trade\BaseTrade.py

from abc import abstractmethod
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class BaseTrade:
    def __init__(self, modules, transaction_type, order_type):
        self.modules = modules
        self.transaction_type = transaction_type
        self.order_type = order_type

    def create_trade_order(self, order_parameters):
        if all(parameter is not None for parameter in order_parameters):
            if self.order_type in [Order_Type.MARKET.value, Order_Type.LIMIT.value, Order_Type.SL.value,
                                   Order_Type.SL_M.value, Order_Type.GTT.value]:
                # Handle various order types
                order_id = self.modules['orders'].initialize(self.order_type, order_parameters)
                return order_id
            else:
                # Handle invalid order type
                log_error("Error: Invalid order type")
                return False
        else:
            # Handle missing common parameters
            log_error("Some required parameters for the order are missing. Order Placement Failed!")
            return False

    def execute_trade(self):
        if self.transaction_type == Transaction_Type.BUY.value:
            return self.buy()
        elif self.transaction_type == Transaction_Type.SELL.value:
            return self.sell()
        else:
            log_error("Error: Invalid transaction type")

    def buy(self):
        raise NotImplementedError("Subclasses must implement buy()")

    def sell(self):
        raise NotImplementedError("Subclasses must implement sell()")

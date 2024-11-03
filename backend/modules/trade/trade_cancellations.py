# TradeCancellations

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from .BaseTrade import BaseTrade
from datetime import datetime, timedelta
from ...controllers.BaseController import BaseController


class TradeCancellations(BaseController, BaseTrade):
    def __init__(self, _base_, parameters):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters

    def initialize(self):
        return self.cancel_aging_trades()

    def cancel_aging_trades(self):
        """ Get Aging Trades """
        # Logic to retrieve active yet to execute orders older than a certain time threshold

        orders_list = self.modules["orders"].initialize(order_type=Order_Type.LIST.value)
        current_time = datetime.now()
        old_aging_orders = []

        # Get open or pending orders which are aging
        for order in orders_list:
            # Check if the order status is "PENDING" or "OPEN"
            if order["status"] == ORDER_IS_OPEN or order["status"] == ORDER_IS_PENDING:
                order_age = current_time - order["order_timestamp"]
                if order_age > timedelta(minutes=ORDER_VALIDITY_THRESHOLD_MINUTES):
                    old_aging_orders.append(order)

        # Cancel the trades
        for order in old_aging_orders:
            self.order_variety = order["variety"]
            self.order_id = order["order_id"]

            order_parameters = [self.order_variety, self.order_id]
            response = self.modules["orders"].initialize(order_type=Order_Type.CANCEL.value, order_parameters=order_parameters)

        # Update Trades Table with CANCEL status
        # Todo: Implement logic to update trades table with CANCEL status

        return True

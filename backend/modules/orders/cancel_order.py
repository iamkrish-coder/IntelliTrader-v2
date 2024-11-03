from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *

import logging


class CancelOrder:
    def __init__(self, order_parameters, prop):
        self.order_parameters = order_parameters
        self.prop = prop

    def initialize(self):
        self.cancel_order()

    def cancel_order(self):
        try:
            self.variety, self.order_id = self.order_parameters
            if self.variety is not None and self.order_id is not None:
                response = self.prop['kite'].cancel_order(variety=self.variety, order_id=self.order_id)
                logging.info(f"Order {self.order_id} has been cancelled successfully.")
            else:
                logging.error("Invalid order parameters provided.")
        except Exception as error:
            logging.error(f"Error cancelling order {self.order_id}: {error}")

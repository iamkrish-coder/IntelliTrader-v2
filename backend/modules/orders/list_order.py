from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
import logging


class ListOrder:

    def __init__(self, prop):
        self.prop = prop

    def initialize(self):
        return self.list_orders()

    def list_orders(self):
        try:
            response = self.prop['kite'].orders()
            logging.info("Fetching Orders List ...COMPLETE!")
            return response
        except Exception as error:
            logging.error(f"Error listing orders: {error}")

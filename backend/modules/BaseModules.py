# backend/modules/BaseModules.py

from .helper.helper_module import Helper
from .fetch.fetch_module import Fetch
from .orders.orders_module import Orders
from .streaming.streaming_module import Ticker
from .indicators.indicators_module import Indicator


class BaseModules:
    def __init__(self, connection):
        self.connection = connection
        self.modules = {'help': Helper(self.connection), 'fetch': Fetch(self.connection),
                        'orders': Orders(self.connection), 'ticker': Ticker(self.connection),
                        'indicator': Indicator(self.connection)}

    def get_module(self, module_name):
        return self.modules.get(module_name)

    def get_all_modules(self):
        return self.modules

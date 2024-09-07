# TradeExecutionController

import asyncio

from source.configurations.shared_parameters import SharedParameters
from source.modules.trade.trade_configurations import TradeConfigurations
from source.modules.trade.trade_signals import TradeSignals
from source.modules.trade.trade_orders import TradeOrders
from ..controllers.BaseController import BaseController
from ..utils.logging_utils import *


class TradeController(BaseController):
    def __init__(self, _base_):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.run_count = 0
        self.parameters = None
        self.alerts = None
        self.publisher = None
        self.signal_event = None
        self.signals = None
        self.signal_ids = None

    async def initialize(self):
        log_info(f"Running Trade ...{self.run_count} Times")
        return await self.trade_handler()

    async def trade_handler(self):
        """
        Orchestrates the execution of a trade, coordinating multiple handlers for various tasks.

        Steps:
        1. Loads trade execution configurations and parameters.
        2. Fetch Signals - Retrieve signals from database
        3. Trade Placement - Place Order and store trade in database
        4. Update Signals - update completed signals in database
        """

        # 1. Load configurations and parameters
        object_configuration_handler = TradeConfigurations(self.configuration)
        settings = object_configuration_handler.initialize()

        object_parameters_handler = SharedParameters(settings)
        object_parameters_handler.initialize()
        self.parameters = object_parameters_handler.get_parameters()

        # 2. Manage Signals - retrieve signals from database
        self.signal_event = SIGNAL_EVENT_GET
        object_signal_handler = TradeSignals(self.modules, self.parameters, self.database, self.signal_event)
        self.signals = object_signal_handler.initialize()

        if self.signals is not None:
            # 3. Trade placement - Place Order and store trade in database
            object_trade_handler = TradeOrders(self.modules, self.parameters, self.database, self.signals)
            self.orders = object_trade_handler.initialize()

            # 4. Update Signals - Update completed signals in database
            self.signal_event = SIGNAL_EVENT_POST
            self.signals = [item['signal_id'] for item in self.signals]
            object_signal_handler = TradeSignals(self.modules, self.parameters, self.database, self.signal_event, self.signals)
            # object_signal_handler.initialize()
        else:
            log_info("No trade signals available at this moment")

        self.run_count += 1

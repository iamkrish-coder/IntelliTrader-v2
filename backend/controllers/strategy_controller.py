# handlers/strategy

import asyncio

from backend.configurations.shared_parameters import SharedParameters
from backend.modules.strategy.strategy_configurations import StrategyConfigurations
from backend.modules.strategy.strategy_candlesticks import StrategyCandlesticks
from backend.modules.strategy.strategy_indicators import StrategyIndicators
from backend.modules.strategy.strategy_market_analysis import StrategyMarketAnalysis
from backend.modules.strategy.strategy_publisher import StrategyPublisher
from backend.modules.strategy.strategy_scanner import StrategyScanner
from backend.modules.strategy.strategy_watchlist import StrategyWatchlist
from backend.controllers.BaseController import BaseController
from backend.utils.logging_utils import *


class StrategyController(BaseController):

    def __init__(self, _base_):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.base_properties = _base_
        self.run_count = 0
        self.parameters = None
        self.alerts = None
        self.publisher = None
        self.watchlist = None
        self.indicators_data_list = None
        self.candlestick_data_list = None

    async def initialize(self):
        log_info(f"Running Strategy...{self.run_count} Times")
        return await self.strategy_handler()

    async def strategy_handler(self):
        """
        Orchestrates the execution of a trading strategy, coordinating multiple handlers for various tasks.

        Steps:
        1. Loads strategy configurations and parameters.
        2. Performs market analysis to determine the current trend.
        3. Manages a watchlist of assets for potential trading opportunities.
        4. Fetches candlestick data for the assets in the watchlist.
        5. Calculates technical indicators based on the candlestick data.
        6. Scans for trading signals based on the indicators and trend.
        7. Publishes alerts for identified trading signals.
        """

        # 1. Load configurations and parameters
        object_configuration_handler = StrategyConfigurations(self.configuration)
        settings = object_configuration_handler.initialize()

        object_parameters_handler = SharedParameters(settings)
        object_parameters_handler.initialize()
        self.parameters = object_parameters_handler.get_parameters()

        # 2. Perform market analysis
        object_market_analysis_handler = StrategyMarketAnalysis(self.base_properties, self.parameters)
        trend = object_market_analysis_handler.initialize()

        # 3. Manage watchlist
        object_watchlist_handler = StrategyWatchlist(self.base_properties, self.parameters)
        self.watchlist = object_watchlist_handler.initialize()

        # 4. Fetch candlestick data
        object_candlesticks_handler = StrategyCandlesticks(self.base_properties, self.parameters, self.watchlist)
        try:
            candlestick_data_fetch_task = asyncio.create_task(
                object_candlesticks_handler.initialize()
            )
            self.candlestick_data_list = await candlestick_data_fetch_task
            if not self.candlestick_data_list:
                log_info("No candlestick data returned. Skipping indicator calculation.")

        except Exception as error:
            print(f"Error fetching candlestick data: {error}. Skipping indicator calculation.")

        else:
            # 5. Calculate indicators
            object_indicators_handler = StrategyIndicators(self.base_properties, self.parameters, self.candlestick_data_list)
            self.indicators_data_list = object_indicators_handler.initialize()

            # 6. Scan for trading signals
            object_scanner_handler = StrategyScanner(self.base_properties, self.parameters, self.candlestick_data_list, self.indicators_data_list)
            self.alerts = object_scanner_handler.initialize()

            # 7. Publish alerts
            self.publisher = SNS
            object_publisher_handler = StrategyPublisher(self.base_properties, self.parameters, self.alerts, self.publisher)
            object_publisher_handler.initialize()

            self.run_count += 1

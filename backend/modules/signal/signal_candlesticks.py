# handlers/signal

import math
import asyncio
from backend.constants.const import *
from backend.controllers.BaseController import BaseController
from backend.enumerations.enums import *
from backend.modules.signal.BaseSignal import BaseSignal
from backend.utils.logging_utils import *


class SignalCandlesticks(BaseController, BaseSignal):
    def __init__(self, _base_, parameters, watchlist):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.trading_watchlist = watchlist
        self.trading_exchange = None
        self.trading_symbol = None
        self.trading_token = None
        self.trading_timeframe = None
        self.timeframe = parameters.get('timeframe')
        self.historical_data_subscription = parameters.get('historical_data_subscription')

    def initialize(self):
        return self.scan_watchlist_stocks()

    async def fetch_ohlc_async(self, trading_exchange, trading_symbol, trading_token, trading_timeframe):
        """
        Fetches OHLC data asynchronously for the given timeframe.
        """
        loop = asyncio.get_running_loop()
        candles = await loop.run_in_executor(None, self.modules['fetch'].fetch_ohlc, trading_exchange, trading_symbol, trading_token, trading_timeframe)
        return candles

    def generate_cache_key(self, exchange, symbol, timeframe):
        """
        Generates a unique cache key based on exchange, symbol, and timeframe.
        """
        return f"{exchange}:{symbol}:{timeframe}"

    async def get_candlestick_information(self):
        """
        Asynchronously fetches OHLC data for different timeframes.
        """
        candlestick_data = {}

        if self.trading_exchange and self.trading_symbol and self.trading_token:
            timeframes = [TODAY_1M, TODAY_2M] # , TODAY_3M
            for timeframe in timeframes:
                candles = await self.fetch_ohlc_async(self.trading_exchange, self.trading_symbol, self.trading_token, timeframe)
                candlestick_data[timeframe] = candles

            return candlestick_data
        else:
            log_error("Required parameters exchange, symbol, token, or timeframe is missing.")
            return None

    async def scan_watchlist_stocks(self):
        """
        Executes the Scanning on Watchlist Instruments.
        """
        candlestick_data_list = []

        try:
            for i, trading_data in enumerate(self.trading_watchlist, start=1):
                self.trading_exchange, self.trading_symbol, self.trading_token = trading_data

                print(f"\nSecondary Scanning Stock {i}/{len(self.trading_watchlist)}: {self.trading_exchange}, {self.trading_symbol}, {self.trading_token}\n")
                log_info(f"Fetching OHLCV data for Secondary Conditions: {self.trading_exchange}, {self.trading_symbol}, {self.trading_token}")

                candlestick_data = await self.get_candlestick_information()

                candlestick_data_list.append({
                    'exchange': self.trading_exchange,
                    'symbol': self.trading_symbol,
                    'token': self.trading_token,
                    'candlestick_data': candlestick_data
                })
        except Exception as error:
            log_error(f"An error occurred while monitoring stock alerts: {str(error)}")

        return candlestick_data_list

# handlers/strategy

import asyncio
import datetime
import time
import os

from concurrent.futures import ThreadPoolExecutor
from backend.constants.const import *
from backend.controllers.BaseController import BaseController
from backend.enumerations.enums import *
from backend.modules.strategy.BaseStrategy import BaseStrategy
from backend.utils.logging_utils import *
from diskcache import Cache


class StrategyCandlesticks(BaseController, BaseStrategy):
    def __init__(self, _base_, parameters, watchlist):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.trading_watchlist = watchlist
        self.trading_exchange = None
        self.trading_symbol = None
        self.trading_token = None
        self.trading_timeframe = None
        self.timeframe = parameters.get('strategy_params.timeframe')
        self.historical_data_subscription = parameters.get('runtime_params.historical_data_subscription')
        self.cache_path = CACHE_PATH
        self.market_start_time = datetime.time(hour=9, minute=15)

    def initialize(self):
        return self.scan_watchlist_stocks()

    async def fetch_ohlc_async(self, trading_exchange, trading_symbol, trading_token, trading_timeframe):
        """
        Fetches OHLC data asynchronously for the given timeframe.
        """
        loop = asyncio.get_running_loop()
        candles = await loop.run_in_executor(None, self.modules['fetch'].fetch_ohlc, trading_exchange, trading_symbol,
                                             trading_token, trading_timeframe)
        return candles

    def generate_cache_key(self, exchange, symbol, timeframe):
        """
        Generates a unique cache key based on exchange, symbol, and timeframe.
        """
        return f"{exchange}:{symbol}:{timeframe}"

    async def get_candlestick_information(self):
        """
        Asynchronously fetches OHLC data for different timeframes, using cache.
        """
        candlestick_data = {}

        # Always fetch data for the user-specified timeframe
        candles = await self.fetch_ohlc_async(self.trading_exchange, self.trading_symbol, self.trading_token, self.timeframe)
        candlestick_data[self.timeframe] = candles

        # Get current date
        now = datetime.datetime.now()
        previous_day = now - datetime.timedelta(days=1)
        current_time = now.time()

        if current_time <= self.market_start_time:
            formatted_date = previous_day.strftime("%Y-%m-%d")
        else:
            formatted_date = now.strftime("%Y-%m-%d")

        # Check if cache directory needs to be updated
        if not os.path.exists(self.cache_path) or self.cache_path.split("/")[-1] != formatted_date:
            # Cache path doesn't exist or date has changed, create new directory
            self.cache_path = os.path.join(CACHE_PATH, formatted_date)
            try:
                os.makedirs(self.cache_path, exist_ok=True)
            except OSError as error:
                print(f"Error creating directory: {error}")

        # Individual cache objects for timeframes
        timeframe_caches = {}

        # Timeframes to cache
        timeframes_to_cache = [DAY, WEEK, MONTH, TODAY_5M]
        """ TODAY_15M, TODAY_30M, TODAY_60M """

        for timeframe in timeframes_to_cache:
            # Create separate cache object for each timeframe
            timeframe_cache_path = os.path.join(self.cache_path, CACHE_CANDLESTICKS_DIR, timeframe.lower())
            os.makedirs(timeframe_cache_path, exist_ok=True)  # Create folder for timeframe
            timeframe_caches[timeframe] = Cache(timeframe_cache_path)

        for timeframe in timeframes_to_cache:
            cache_key = self.generate_cache_key(self.trading_exchange, self.trading_symbol, timeframe)

            # Check if first candle is complete (relevant for TODAY_* timeframes)
            if timeframe.startswith("today"):

                minutes = int((timeframe.split("today")[1]).split("minute")[0])
                target_time = datetime.datetime.combine(now.date(), self.market_start_time)
                target_time += datetime.timedelta(minutes=minutes)

                # Check if current time is past the target time
                if current_time >= target_time.time():
                    cached_data = timeframe_caches[timeframe].get(cache_key)
                    if cached_data is not None:
                        candlestick_data[timeframe] = cached_data
                    else:
                        candles = await self.fetch_ohlc_async(self.trading_exchange, self.trading_symbol,
                                                              self.trading_token, timeframe)
                        candlestick_data[timeframe] = candles
                        timeframe_caches[timeframe].set(cache_key, candles)
                else:
                    cached_data = timeframe_caches[timeframe].get(cache_key)
                    if cached_data is not None:
                        candlestick_data[timeframe] = cached_data
                    elif current_time <= self.market_start_time:
                        candles = await self.fetch_ohlc_async(self.trading_exchange, self.trading_symbol,
                                                              self.trading_token, timeframe)
                        candlestick_data[timeframe] = candles
                        timeframe_caches[timeframe].set(cache_key, candles)
                    else:
                        log_warn(
                            f"Waiting for {timeframe} live data to be available after market opens, using previous day data...")

            else:
                # DAILY, WEEKLY and MONTHLY timeframe, proceed with regular cache operations
                cached_data = timeframe_caches[timeframe].get(cache_key)
                if cached_data is not None:
                    candlestick_data[timeframe] = cached_data
                else:
                    # Fetch data if not cached
                    candles = await self.fetch_ohlc_async(self.trading_exchange, self.trading_symbol,
                                                          self.trading_token, timeframe)
                    candlestick_data[timeframe] = candles
                    timeframe_caches[timeframe].set(cache_key, candles)

        return candlestick_data

    async def scan_watchlist_stocks(self):
        """
        Executes the Scanning on Watchlist Instruments.
        """
        candlestick_data_list = []

        try:
            for i, stock in enumerate(self.trading_watchlist, start=1):

                self.trading_exchange = stock.get('exchange')
                self.trading_symbol = stock.get('tradingsymbol')
                if self.trading_exchange is None or self.trading_symbol is None:
                    continue
                self.trading_token = stock.get('instrument_token') if stock.get('instrument_token') else self.modules[
                    'fetch'].trading_token_lookup(self.trading_exchange, self.trading_symbol)

                # Create stock data dictionary for this stock
                stock_data = {
                    'exchange': self.trading_exchange,
                    'symbol': self.trading_symbol,
                    'token': self.trading_token
                }

                print(f"\nPrimary Scanning Stock {i}/{len(self.trading_watchlist)}: {self.trading_exchange}, {self.trading_symbol}, {self.trading_token}\n")
                log_info(f"Fetching OHLCV data for Primary Conditions: {self.trading_exchange}, {self.trading_symbol}, {self.trading_token}")

                candlestick_data = await self.get_candlestick_information()

                candlestick_data_list.append({
                    'exchange': self.trading_exchange,
                    'symbol': self.trading_symbol,
                    'token': self.trading_token,
                    'candlestick_data': candlestick_data
                })

        except Exception as error:
            log_error(f"An error occurred while scanning watchlist stocks: {str(error)}")

        return candlestick_data_list

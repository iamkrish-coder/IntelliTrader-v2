# strategies/shared_functions.py

import pandas as pd
import numpy as np
import yfinance as yf
import calendar
import math
import hashlib
import datetime
import json
import uuid
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class SharedFunctions:
    def __init__(self, modules=None):
        self.cache_path = CACHE_PATH
        self.modules = modules

    def generate_table_uid(self, table_name):
        if table_name:
            table_prefix = table_name[:3].upper()
            return table_prefix + datetime.datetime.now().strftime("%y%m%d%H%M%S")
        else:
            log_error("Invalid table")
            return None

    def is_red(self, candle):
        return candle['close'] < candle['open']

    def is_green(self, candle):
        return candle['close'] > candle['open']

    def is_doji(self, candle, threshold=0.01):
        return abs(candle['close'] - candle['open']) < threshold * self.calculate_candle_range(candle)

    def is_higher_high(self, candle, previous_candle):
        return candle['high'] > previous_candle['high']

    def is_lower_low(self, candle, previous_candle):
        return candle['low'] < previous_candle['low']

    def is_engulfing_pattern(self, candle, previous_candle):
        return candle['high'] > previous_candle['high'] and candle['low'] < previous_candle['low']

    def is_hammer(self, candle):
        body_size = abs(candle['close'] - candle['open'])
        upper_shadow = candle['high'] - max(candle['open'], candle['close'])
        lower_shadow = min(candle['open'], candle['close']) - candle['low']
        return upper_shadow >= 2 * body_size and lower_shadow <= body_size

    def is_shooting_star(self, candle):
        body_size = abs(candle['close'] - candle['open'])
        upper_shadow = candle['high'] - max(candle['open'], candle['close'])
        lower_shadow = min(candle['open'], candle['close']) - candle['low']
        return upper_shadow >= 2 * body_size and lower_shadow >= body_size

    def is_inside_bar(self, candle, previous_candle):
        return candle['high'] < previous_candle['high'] and candle['low'] > previous_candle['low']

    def is_bearish_engulfing(self, candle, previous_candle):
        return candle['close'] < candle['open'] and previous_candle['close'] < previous_candle['open'] and \
            candle['open'] >= previous_candle['close'] and candle['close'] <= previous_candle['open']

    def is_bearish_engulfing(self, candle, previous_candle):
        return candle['close'] < candle['open'] and previous_candle['close'] < previous_candle['open'] and \
            candle['open'] >= previous_candle['close'] and candle['close'] <= previous_candle['open']

    def is_bullish_harami(self, candle, previous_candle):
        return previous_candle['close'] > previous_candle['open'] and candle['close'] > candle['open'] and \
            candle['open'] < previous_candle['close'] and candle['close'] > previous_candle['open']

    def is_bearish_harami(self, candle, previous_candle):
        return previous_candle['close'] < previous_candle['open'] and candle['close'] < candle['open'] and \
            candle['open'] > previous_candle['close'] and candle['close'] < previous_candle['open']

    def calculate_candle_range(self, candle):
        return candle['high'] - candle['low']

    def calculate_candle_body_size(self, candle):
        return abs(candle['close'] - candle['open'])

    def calculate_candle_wick_size(self, candle):
        return max(candle['high'] - max(candle['open'], candle['close']),
                   max(candle['open'], candle['close']) - candle['low'])

    def get_last_n_candles(self, candles, n):
        """
        Get the last n candles from the given candle dataset.
        """
        return candles.iloc[-n:]

    def get_first_candle_of_day(self, candles):
        """
        Get the first candle of the day from the given candle dataset.
        """
        return candles.iloc[0] if candles else None

    def get_nth_last_prices(self, candles, n=1):
        """
        Get the nth last open, high, low, close, and volume from the dataset.
        """
        if not candles.empty and len(candles) >= n:
            nth_last_candle = candles.iloc[-n]
            nth_last_open = nth_last_candle.get('open')
            nth_last_high = nth_last_candle.get('high')
            nth_last_low = nth_last_candle.get('low')
            nth_last_close = nth_last_candle.get('close')
            nth_last_volume = nth_last_candle.get('volume')
            return nth_last_open, nth_last_high, nth_last_low, nth_last_close, nth_last_volume
        else:
            return None, None, None, None, None

    def get_nth_first_prices(self, candles, n=1):
        """
        Get the nth first open, high, low, close, and volume from the dataset.
        """
        if not candles.empty and len(candles) >= n:
            nth_first_candle = candles.iloc[n - 1]
            nth_first_open = nth_first_candle.get('open')
            nth_first_high = nth_first_candle.get('high')
            nth_first_low = nth_first_candle.get('low')
            nth_first_close = nth_first_candle.get('close')
            nth_first_volume = nth_first_candle.get('volume')
            return nth_first_open, nth_first_high, nth_first_low, nth_first_close, nth_first_volume
        else:
            return None, None, None, None, None

    def get_local_market_sentiment(self):
        pass

    def get_global_market_sentiment(self):
        pass

    def get_first_candle_data(self, candles, period):
        try:
            # return [value.item() for value in self.get_nth_first_prices(candles, period)]
            return {
                "open": self.get_nth_first_prices(candles, period)[0].item(),
                "high": self.get_nth_first_prices(candles, period)[1].item(),
                "low": self.get_nth_first_prices(candles, period)[2].item(),
                "close": self.get_nth_first_prices(candles, period)[3].item(),
                "volume": self.get_nth_first_prices(candles, period)[4].item()
            }
        except (AttributeError, ValueError, TypeError):
            return None

    def get_last_candle_data(self, candles, period):
        try:
            # return [value.item() for value in self.get_nth_last_prices(candles, period)]
            return {
                "open": self.get_nth_last_prices(candles, period)[0].item(),
                "high": self.get_nth_last_prices(candles, period)[1].item(),
                "low": self.get_nth_last_prices(candles, period)[2].item(),
                "close": self.get_nth_last_prices(candles, period)[3].item(),
                "volume": self.get_nth_last_prices(candles, period)[4].item()
            }
        except (AttributeError, ValueError, TypeError):
            return None

    def process_current_candles(self, candles_current):
        ohlcv_current_data = {}
        # Current Interval Candles
        ohlcv_current_data['open'] = candles_current.get('open', []).tolist()
        ohlcv_current_data['high'] = candles_current.get('high', []).tolist()
        ohlcv_current_data['low'] = candles_current.get('low', []).tolist()
        ohlcv_current_data['close'] = candles_current.get('close', []).tolist()
        ohlcv_current_data['volume'] = candles_current.get('volume', []).tolist()

        return ohlcv_current_data

    def process_daily_candles(self, candles_daily):
        ohlcv_daily_data = {}
        # Daily Candles
        ohlcv_daily_data['open'] = candles_daily.get('open', []).tolist()
        ohlcv_daily_data['high'] = candles_daily.get('high', []).tolist()
        ohlcv_daily_data['low'] = candles_daily.get('low', []).tolist()
        ohlcv_daily_data['close'] = candles_daily.get('close', []).tolist()
        ohlcv_daily_data['volume'] = candles_daily.get('volume', []).tolist()

        return ohlcv_daily_data

    def process_weekly_candles(self, candles_weekly):
        ohlcv_weekly_data = {}
        # Weekly Candles
        ohlcv_weekly_data['open'] = candles_weekly.get('open', []).tolist()
        ohlcv_weekly_data['high'] = candles_weekly.get('high', []).tolist()
        ohlcv_weekly_data['low'] = candles_weekly.get('low', []).tolist()
        ohlcv_weekly_data['close'] = candles_weekly.get('close', []).tolist()
        ohlcv_weekly_data['volume'] = candles_weekly.get('volume', []).tolist()

        return ohlcv_weekly_data

    def process_monthly_candles(self, candles_monthly):
        ohlcv_monthly_data = {}
        # Monthly Candles
        ohlcv_monthly_data['open'] = candles_monthly.get('open', []).tolist()
        ohlcv_monthly_data['high'] = candles_monthly.get('high', []).tolist()
        ohlcv_monthly_data['low'] = candles_monthly.get('low', []).tolist()
        ohlcv_monthly_data['close'] = candles_monthly.get('close', []).tolist()
        ohlcv_monthly_data['volume'] = candles_monthly.get('volume', []).tolist()

        return ohlcv_monthly_data

    def process_today_candles(self, candles_today):
        ohlcv_today_data = {}
        # Today Candles
        ohlcv_today_data['open'] = candles_today.get('open', []).tolist()
        ohlcv_today_data['high'] = candles_today.get('high', []).tolist()
        ohlcv_today_data['low'] = candles_today.get('low', []).tolist()
        ohlcv_today_data['close'] = candles_today.get('close', []).tolist()
        ohlcv_today_data['volume'] = candles_today.get('volume', []).tolist()

        return ohlcv_today_data

    def get_duration_week(self, depth=1):
        today = datetime.date.today()
        current_year = today.year
        current_month = today.month
        current_day = today.weekday()

        duration = 0
        for i in range(0, depth):
            days_in_week = 7
            if i == 0:
                days_in_current_week = today.weekday() + 1
                duration = days_in_current_week
            else:
                duration += days_in_week

        return duration

    def get_duration_month(self, depth=1):
        today = datetime.date.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        # Get the number of days in the current month
        duration = 0
        for i in range(1, depth):
            month = 12 if current_month - i == 0 else current_month - i
            days_in_month = calendar.monthrange(current_year, month)[1]
            if i == 0:
                weekends_in_month = (int(current_day) // 7) * 2
                duration = current_day
            else:
                weekends_in_month = (int(days_in_month) // 7) * 2
                duration += days_in_month

        return duration

    # def get_underlying_ltp(self, ticker):
    #     stock = ticker if ticker not in ('NIFTY', 'BANKNIFTY') else None
    #
    #     if ticker == 'NIFTY':
    #         underlying = '^NSEI'
    #     elif ticker == 'BANKNIFTY':
    #         underlying = '^NSEBANK'
    #     elif stock is not None:
    #         underlying = stock + '.NS'
    #     else:
    #         log_error("The derivative instrument provided is invalid")
    #         return False
    #
    #     hist_data = yf.download(underlying, period='5d')
    #     underlying_current_price = hist_data['Adj Close'].iloc[-1]
    #     return underlying_current_price


    # def get_option_contracts(self, dump, ticker, strike):
    #     contracts = []
    #     for instrument in dump:
    #         if instrument['name'] == ticker or instrument['tradingsymbol'] == ticker and instrument['instrument_type'] == strike:
    #             contracts.append(instrument)
    #     return pd.DataFrame(contracts)

    def generate_record_hash(self, record):
        # Create a unique hash from the string data
        hash_object = hashlib.sha256(record.encode("utf-8"))
        return hash_object.hexdigest()

    def get_current_timestamp(self):
        current_timestamp = datetime.datetime.now(datetime.timezone.utc)
        formatted_timestamp = current_timestamp.strftime("%Y%m%d%H%M")
        return formatted_timestamp

    def generate_aws_sns_topic_name(self, strategy_id):
        if strategy_id is None:
            log_error("Strategy ID cannot be None")
        return f"T-STR-{strategy_id}"

    def generate_aws_sns_topic_details(self, strategy_id, topic_type=None):

        # ARN Template: arn:aws:sns:<region>:<account-id>:<topic-name>
        topic_name = self.generate_aws_sns_topic_name(strategy_id)

        enum_arn = AWS_SNS.ARN.value
        enum_aws = AWS_SNS.AWS.value
        enum_sns = AWS_SNS.SNS.value
        enum_region = AWS_SNS.REGION.value
        enum_account_id = AWS_SNS.ACCOUNT_ID.value
        enum_topic_name = topic_name

        if topic_type == FIFO:
            topic_name = topic_name + ".fifo"
            arn_formatted = f"{enum_arn}:{enum_aws}:{enum_sns}:{enum_region}:{enum_account_id}:{enum_topic_name}" + ".fifo"
        else:
            arn_formatted = f"{enum_arn}:{enum_aws}:{enum_sns}:{enum_region}:{enum_account_id}:{enum_topic_name}"

        return arn_formatted, topic_name

    def get_aws_sqs_queue_name(self, strategy_id):
        if strategy_id is None:
            log_error("Strategy ID cannot be None")
        return f"Q-STR-{strategy_id}"

    def generate_aws_sqs_queue_details(self, strategy_id, queue_type=None):

        # ARN Template: arn:aws:sns:<region>:<account-id>:<topic-name>
        queue_name = self.get_aws_sqs_queue_name(strategy_id)
        queue_url = self.get_aws_sqs_queue_url(queue_name)

        enum_arn = AWS_SQS.ARN.value
        enum_aws = AWS_SQS.AWS.value
        enum_sqs = AWS_SQS.SQS.value
        enum_region = AWS_SQS.REGION.value
        enum_account_id = AWS_SQS.ACCOUNT_ID.value
        enum_queue_name = queue_name

        if queue_type == FIFO:
            queue_name = queue_name + ".fifo"
            queue_arn_formatted = f"{enum_arn}:{enum_aws}:{enum_sqs}:{enum_region}:{enum_account_id}:{enum_queue_name}" + ".fifo"
            queue_url = queue_url + ".fifo"
        else:
            queue_arn_formatted = f"{enum_arn}:{enum_aws}:{enum_sqs}:{enum_region}:{enum_account_id}:{enum_queue_name}"

        return queue_arn_formatted, queue_name, queue_url

    def get_aws_sqs_queue_url(self, queue_name):
        # Get the SQS queue URL
        queue_url = f'{AWS_SQS.URL.value}/{AWS_SQS.ACCOUNT_ID.value}/{queue_name}'
        return queue_url

    def generate_strategy_details(self, filename):
        if os.path.isfile(os.path.join(ALGORITHM_PATH, filename)) and not filename.startswith('.'):
            strategy_name = os.path.splitext(filename)[0]
            parts = strategy_name.split('-')

            # Check if the split length matches the expected format (4 parts)
            if len(parts) < 4:
                log_error(f"Warning: Unexpected format for strategy name: {strategy_name}")
                return

            strategy_id, strategy_name, strategy_type, strategy_description = parts[1], parts[2], parts[3], parts[4]
            return strategy_id, strategy_name, strategy_type, strategy_description

    def generate_group_id(self, strategy_id):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
        return f"{strategy_id}-{timestamp}"

    def calculate_quantity_per_allocation(self, max_allocation, stock_last_traded_price, lot_size):
        try:
            max_allocation = float(max_allocation)
            stock_last_traded_price = float(stock_last_traded_price)

            # Calculate the quantity of stocks based on maximum allocation
            quantity = max_allocation / (stock_last_traded_price * lot_size)
            return quantity
        except ValueError:
            # Handle the case where the inputs are not valid numbers
            return None

    def calculate_quantity_per_risk(self, max_risk, stock_last_traded_price, lot_size, stop_loss_percentage=0.5):
        try:
            max_risk = float(max_risk)
            stock_last_traded_price = float(stock_last_traded_price)
            stop_loss_percentage = float(stop_loss_percentage)

            # Calculate the stop-loss price based on the percentage
            stop_loss_price = stock_last_traded_price * (1 - stop_loss_percentage)

            # Calculate the risk per share
            risk_per_share = stock_last_traded_price - stop_loss_price

            # Calculate the quantity of stocks based on maximum risk
            quantity = max_risk / (risk_per_share * lot_size)

            return quantity
        except ValueError:
            # Handle the case where the inputs are not valid numbers
            return None

    def set_quantity(self, exchange, symbol, max_quantity, position_size_type, max_allocation, max_risk, lot_size=1):
        if self.modules is None:
            log_error("Error: Modules is not initialized")
            return None

        if exchange is None or symbol is None:
            log_error("Error: Exchange and Symbol cannot be None")
            return None

        if position_size_type == Position_Size.CAPITAL_BASED.value:
            ltp = self.modules['fetch'].fetch_ltp(exchange, symbol)
            quantity = math.floor(self.calculate_quantity_per_allocation(max_allocation, ltp, lot_size))
        elif position_size_type == Position_Size.RISK_BASED.value:
            ltp = self.modules['fetch'].fetch_ltp(exchange, symbol)
            quantity = math.floor(self.calculate_quantity_per_risk(max_risk, ltp, lot_size))
        elif position_size_type == Position_Size.MANUAL.value:
            quantity = int(1)
        else:
            log_error("Error: Invalid position_size_type")
            return None

        if max_quantity < quantity:
            quantity = max_quantity

        if lot_size:
            quantity = quantity * lot_size

        return quantity

    def set_limit_price(self, exchange, symbol, default_price_enum, limit_buffer):
        """Sets the limit price for a trade.

        Args:
            exchange (str): The exchange where the trade will be executed.
            symbol (str): The symbol of the instrument being traded.
            default_price (float): The default price to be used.
            limit_buffer (float): The buffer to be added to or subtracted from the default price.

        Returns:
            float: The calculated limit price.
        """
        if self.modules is None:
            log_error("Error: Modules is not initialized")
            return None

        # Fetch the stock value based on the enum value
        if default_price_enum == Default_Price_Limit.LTP.value:
            stock_value = self.modules['fetch'].fetch_ltp(exchange, symbol)
        else:
            # Handle invalid default_price_enum
            raise ValueError("Invalid default_price_enum")

        if limit_buffer > 0:
            limit_price = stock_value + limit_buffer
        elif limit_buffer < 0:
            limit_price = stock_value - abs(limit_buffer)
        else:
            limit_price = stock_value

        return limit_price

    def set_trigger_price(self, exchange, symbol):
        pass

    def check_cache_path_exists(self):
        # Get current date
        market_start_time = datetime.time(hour=9, minute=15)
        now = datetime.datetime.now()
        previous_day = now - datetime.timedelta(days=1)
        current_time = now.time()

        if current_time <= market_start_time:
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

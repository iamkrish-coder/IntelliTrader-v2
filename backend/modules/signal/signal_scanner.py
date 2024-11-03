# handlers/signal
import json

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from .BaseSignal import BaseSignal
from ...controllers.BaseController import BaseController


class SignalScanner(BaseController, BaseSignal):
    def __init__(self, _base_, parameters, candlesticks_data_list, candles_timeframe=None):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.candlesticks_data_list = candlesticks_data_list
        self.candles_timeframe = candles_timeframe or self.parameters['strategy_params.timeframe']
        self.strategy_id = self.parameters['strategy_params.strategy_id']
        self.strategy_type = int(self.parameters['strategy_params.strategy_type'])
        self.strategy_definition = self.get_strategy_definition()
        self.signal_type = None

    def initialize(self):
        return self.scan_secondary_conditions()

    def get_strategy_definition(self):
        strategy_contents = None
        strategy_type_enum = Strategy_Type(self.strategy_type)
        strategy_type_description = strategy_type_enum.name

        for filename in os.listdir(ALGORITHM_PATH):
            if filename.startswith(f"STR-000-Secondary-{strategy_type_description.capitalize()}"):
                strategy_file = os.path.join(ALGORITHM_PATH, filename)
                with open(strategy_file, 'r') as f:
                    strategy_contents = json.load(f)
        return strategy_contents

    def scan_secondary_conditions(self):
        results = []
        alert_signals = {}
        for stock_index, (candlestick_data) in enumerate(self.candlesticks_data_list):

            exchange = candlestick_data['exchange']
            symbol = candlestick_data['symbol']
            token = candlestick_data['token']

            conditions = self.parse_strategy(self.strategy_definition, StrategyDefinition.BUY.value)
            candlesticks = self.parse_candlesticks(candlestick_data)
            self.signal_type = Transaction_Type.BUY.value

            for condition in conditions:
                condition_result = self.evaluate_condition(condition, candlesticks)
                if not condition_result:
                    break  # If any condition fails, break the loop
                else:
                    message = f"{exchange}, {symbol}, {token}"
                    results.append(message)
        return {
            "strategy_id": self.strategy_id,
            "signal_type": self.signal_type,
            "results": results
        }

    def parse_strategy(self, strategy_definition, section):
        conditions = strategy_definition['strategy'][section]['conditions']
        return conditions

    def parse_candlesticks(self, candlesticks_data_list):
        candle_data = {}
        try:
            # Extracting candlestick data
            candles_today_1m = None
            candles_today_2m = None
            candles_today_3m = None

            candles_today_1m = candlesticks_data_list['candlestick_data'][TODAY_1M]  # First dataframe
            candles_today_2m = candlesticks_data_list['candlestick_data'][TODAY_2M]  # Second dataframe
            # candles_today_3m = candlesticks_data_list['candlestick_data'][TODAY_3M]  # Third dataframe

            candle_data['1minute(-1)'] = self.get_last_candle_data(candles_today_1m, 1)
            candle_data['2minute(-1)'] = self.get_last_candle_data(candles_today_2m, 1)
            # candle_data['3minute(-1)'] = self.get_last_candle_data(candles_today_3m, 1)

            candle_data['1minute(-2)'] = self.get_last_candle_data(candles_today_1m, 2)
            candle_data['2minute(-2)'] = self.get_last_candle_data(candles_today_2m, 2)
            # candle_data['3minute(-2)'] = self.get_last_candle_data(candles_today_3m, 2)

            return candle_data

        except Exception as error:
            log_error(f"An error occurred while evaluating secondary conditions: {str(error)}")

    def evaluate_condition(self, condition, candlestick_data):
        """Evaluates a single condition.
        Args:
          condition: The condition to evaluate.
          candlestick_data: The candlestick data to evaluate.

        Returns:
          True if the condition is met, False otherwise.
        """
        if 'type' in condition:
            if condition['type'] == 'AND':
                return all(self.evaluate_condition(cond, candlestick_data) for cond in condition['rules'])
            elif condition['type'] == 'OR':
                return any(self.evaluate_condition(cond, candlestick_data) for cond in condition['rules'])
        else:
            # Base condition
            if 'candle' in condition:
                timeframe = condition['candle']
                shift = condition['shift']
                candle = self.get_candle_value(candlestick_data, timeframe, shift)
                prev_candle = self.get_candle_value(candlestick_data, timeframe, shift - 1)

                if candle is not None:
                    if 'is red' in condition['value']:
                        result = self.is_red(candle)
                    elif 'is green' in condition['value']:
                        result = self.is_green(candle)
                    elif 'is bearish harami' in condition['value']:
                        result = self.is_bearish_harami(candle, prev_candle)
                    elif 'is bullish harami' in condition['value']:
                        result = self.is_bullish_harami(candle, prev_candle)
                    elif 'is bearish engulfing' in condition['value']:
                        result = self.is_bearish_engulfing(candle, prev_candle)
                    elif 'is inside bar' in condition['value']:
                        result = self.is_inside_bar(candle, prev_candle)
                    elif 'is shooting star' in condition['value']:
                        result = self.is_shooting_star(candle)
                    elif 'is hammer' in condition['value']:
                        result = self.is_hammer(candle)
                    elif 'is engulfing pattern' in condition['value']:
                        result = self.is_engulfing_pattern(candle, prev_candle)
                    elif 'is lower low' in condition['value']:
                        result = self.is_lower_low(candle, prev_candle)
                    elif 'is higher high' in condition['value']:
                        result = self.is_higher_high(candle, prev_candle)
                    elif 'is doji' in condition['value']:
                        result = self.is_doji(candle)
                    else:
                        log_info(f"Unsupported candle condition: {condition}")
                        result = False
                    return result
            else:
                print(condition)

    def get_candle_value(self, candlestick_data, timeframe, shift):
        """Extracts candle data based on timeframe and shift.
            Args:
                candlestick_data: The candlestick data dictionary.
                timeframe: The timeframe string (e.g., "default").
                shift: The shift value (e.g., -1).

            Returns:
                The extracted candle data or None if not found.
            """
        key = f"{timeframe}({shift})"
        if key in candlestick_data:
            return candlestick_data[key]
        else:
            return None

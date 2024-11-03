# handlers/strategy
import json

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from .BaseStrategy import BaseStrategy
from ...controllers.BaseController import BaseController
import re


class StrategyScanner(BaseController, BaseStrategy):
    def __init__(self, _base_, parameters, candlesticks_data_list, indicators_data_list, candles_timeframe=None):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.candlesticks_data_list = candlesticks_data_list
        self.indicators_data_list = indicators_data_list
        self.candles_timeframe = candles_timeframe or self.parameters['strategy_params.timeframe']
        self.strategy_id = self.parameters['strategy_params.strategy_id']
        self.strategy_type = self.parameters['strategy_params.strategy_type']
        self.strategy_definition = self.get_strategy_definition()

    def initialize(self):
        return self.scan_primary_conditions()

    def get_strategy_definition(self):
        strategy_contents = None
        selected_strategy = self.strategy_id.zfill(3)
        for filename in os.listdir(ALGORITHM_PATH):
            if filename.startswith(f"STR-{selected_strategy}"):
                strategy_file = os.path.join(ALGORITHM_PATH, filename)
                with open(strategy_file, 'r') as f:
                    strategy_contents = json.load(f)
        return strategy_contents

    def scan_primary_conditions(self):
        results = []
        for stock_index, (candlestick_data, indicator_data) in enumerate(zip(self.candlesticks_data_list, self.indicators_data_list)):

            exchange = candlestick_data['exchange']
            symbol = candlestick_data['symbol']
            token = candlestick_data['token']

            conditions = self.parse_strategy(self.strategy_definition, StrategyDefinition.BUY.value)
            candlesticks = self.parse_candlesticks(candlestick_data)
            indicators = self.parse_indicators(indicator_data)

            for condition in conditions:
                condition_result = self.evaluate_condition(condition, candlesticks, indicators)
                if not condition_result:
                    break  # If any condition fails, break the loop
                else:
                    message = f"{exchange}, {symbol}, {token}"
                    results.append(message)
        return results

    def parse_strategy(self, strategy_definition, section):
        conditions = strategy_definition['strategy'][section]['conditions']
        return conditions

    def parse_candlesticks(self, candlesticks_data_list):
        candle_data = {}
        try:
            # Extracting candlestick data
            candles = None
            candles_daily = None
            candles_weekly = None
            candles_monthly = None
            candles_today_5m = None
            candles_today_15m = None
            candles_today_30m = None
            candles_today_60m = None

            candles = candlesticks_data_list['candlestick_data'][self.candles_timeframe]  # First dataframe
            candles_daily = candlesticks_data_list['candlestick_data'][DAY]               # Second dataframe
            candles_weekly = candlesticks_data_list['candlestick_data'][WEEK]             # Third dataframe
            candles_monthly = candlesticks_data_list['candlestick_data'][MONTH]           # Fourth dataframe
            candles_today_5m = candlesticks_data_list['candlestick_data'][TODAY_5M]       # Fifth dataframe
            # candles_today_15m = candlesticks_data_list['candlestick_data'][TODAY_15M]   # Sixth dataframe
            # candles_today_30m = candlesticks_data_list['candlestick_data'][TODAY_30M]   # Seventh dataframe
            # candles_today_60m = candlesticks_data_list['candlestick_data'][TODAY_60M]   # Eighth dataframe

            candle_data['5minute(1)'] = self.get_first_candle_data(candles_today_5m, 1)
            # candle_data['15minute(1)'] = self.get_first_candle_data(candles_today_15m, 1)
            # candle_data['30minute(1)'] = self.get_first_candle_data(candles_today_30m, 1)
            # candle_data['60minute(1)'] = self.get_first_candle_data(candles_today_60m, 1)

            candle_data['default(-1)'] = self.get_last_candle_data(candles, 1)
            candle_data['daily(-1)'] = self.get_last_candle_data(candles_daily, 1)
            candle_data['weekly(-1)'] = self.get_last_candle_data(candles_weekly, 1)
            candle_data['monthly(-1)'] = self.get_last_candle_data(candles_monthly, 1)

            candle_data['default(-2)'] = self.get_last_candle_data(candles, 2)
            candle_data['daily(-2)'] = self.get_last_candle_data(candles_daily, 2)
            candle_data['weekly(-2)'] = self.get_last_candle_data(candles_weekly, 2)
            candle_data['monthly(-2)'] = self.get_last_candle_data(candles_monthly, 2)

            candle_data['default(-3)'] = self.get_last_candle_data(candles, 3)
            candle_data['daily(-3)'] = self.get_last_candle_data(candles_daily, 3)
            candle_data['weekly(-3)'] = self.get_last_candle_data(candles_weekly, 3)
            candle_data['monthly(-3)'] = self.get_last_candle_data(candles_monthly, 3)

            return candle_data

        except Exception as error:
            log_error(f"An error occurred while evaluating primary conditions: {str(error)}")

    def parse_indicators(self, indicators_data_list):
        return indicators_data_list['indicators_data']

    def evaluate_condition(self, condition, candlestick_data, indicator_data):
        """Evaluates a single condition.
        Args:
          condition: The condition to evaluate.
          candlestick_data: The candlestick data to evaluate.
          indicator_data: The indicators data to evaluate.

        Returns:
          True if the condition is met, False otherwise.
        """
        if 'type' in condition:
            if condition['type'] == 'AND':
                return all(self.evaluate_condition(cond, candlestick_data, indicator_data) for cond in condition['rules'])
            elif condition['type'] == 'OR':
                return any(self.evaluate_condition(cond, candlestick_data, indicator_data) for cond in condition['rules'])
        else:
            # Base condition
            if 'indicator' in condition:
                indicator_value = self.get_indicator_value(indicator_data, condition['indicator'].lower(), condition['period'], condition['shift'])
                sub_indicator_value = self.get_indicator_value(indicator_data, condition['indicator'].lower(), condition['period'], condition['shift'])
                return eval(f"{indicator_value} {condition['operator']} {condition['value']}")
            elif 'candle' in condition:
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

    def get_indicator_value(self, data, indicator, period, shift):
        """Fetches the indicator value from data backend.
        Args:
          data: The Datasource
          indicator: The indicator name.
          period: The indicator period.
          shift: The indicator shift.

        Returns:
          The calculated indicator value.
        """
        value = data[indicator][shift]
        return value

    def parse_strategy_deprecated(self, strategy_definition, section):
        conditions = []
        section_header_pattern = r"^(Buy|Sell|Exit|SL|TSL) When:$"
        section_pattern = r"^" + section.value + r" When:$"
        current_section = None

        for line in strategy_definition.splitlines():
            line = line.strip()
            if not line:
                continue

            # Check if line matches the section pattern
            match = re.match(section_header_pattern, line)
            if match:
                if re.match(section_pattern, line):
                    current_section = section.value + " When:"
                    continue
                else:
                    current_section = None

            # Process conditions within the desired section
            if current_section == section.value + " When:":
                # match = re.match(r"indicator (\w+)(?: \((\d+)\))? (>|<|>=|<=|=|\!=) (\d+)", line)
                # Indicator condition
                match = re.match(r"indicator (\w+)\s*\((\d+)\)\s*(>|<=|<|>=|=|\!=)\s*(\d+)", line, re.IGNORECASE)
                if match:
                    indicator, period, operator, value = match.groups()
                    conditions.append((indicator, int(period) if period else None, operator, int(value)))

                # Candle condition
                match = re.match(r"candle \((\d+)\) (=|\!=) (red|green)", line, re.IGNORECASE)
                if match:
                    offset, operator, color = match.groups()
                    conditions.append(("candle", int(offset), operator, color))

# handlers/strategy

from backend.constants.const import *
from backend.controllers.BaseController import BaseController
from backend.enumerations.enums import *
from backend.modules.strategy.BaseStrategy import BaseStrategy
from backend.utils.logging_utils import *


class StrategyIndicators(BaseController, BaseStrategy):
    def __init__(self, _base_, parameters, candlestick_data, candles_timeframe=None):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.candlesticks_data = candlestick_data
        self.candles_timeframe = candles_timeframe or self.parameters['strategy_params.timeframe']

    def initialize(self):
        return self.calculate_indicators()

    def get_indicator_values(self, indicator, datasource, setting):
        indicator_values = self.modules['indicator'].use_indicator(indicator, datasource, setting)
        return indicator_values

    def calculate_indicators(self):
        """
        Calculates and stores various technical indicators for the given OHLCV data.

        Args:

        Returns:
            dict: A dictionary containing calculated indicator values along with other information.
        """
        # Initialize an empty list to store results for each instrument
        indicator_data_list = []

        for result in self.candlesticks_data:
            exchange = result['exchange']
            symbol = result['symbol']
            token = result['token']
            candlestick_data_all_timeframes = result['candlestick_data']
            candles = candlestick_data_all_timeframes[self.candles_timeframe]

            indicator_data = {
                                'rsi': self.get_indicator_values('rsi', candles, RSI.RSI_8.value),
                                'wma5': self.get_indicator_values('wma', candles, WMA.WMA_5.value),
                                'wma20': self.get_indicator_values('wma', candles, WMA.WMA_21.value),
                                'supertrend': self.get_indicator_values('supertrend', candles, Supertrend.SUPERTREND_4_2.value),
                                'truerange': self.get_indicator_values('truerange', candles, TrueRange.TRUERANGE_14.value),
                                'average_truerange': self.get_indicator_values('average_truerange', candles, AverageTrueRange.AVERAGETRUERANGE_14.value),
                                'macd': self.get_indicator_values('macd', candles, MACD.MACD_12_26_9.value)
                              }

            # Check if any indicator data is None, if so, skip adding it to the list
            if all(value is not None for value in indicator_data.values()):
                indicator_data_list.append({
                    'exchange': exchange,
                    'symbol': symbol,
                    'token': token,
                    'indicators_data': indicator_data
                })

        return indicator_data_list

# handlers/strategy

from backend.constants.const import *
from backend.controllers.BaseController import BaseController
from backend.enumerations.enums import *
from backend.modules.strategy.BaseStrategy import BaseStrategy
from backend.utils.logging_utils import *


class StrategyMarketAnalysis(BaseController, BaseStrategy):
    def __init__(self, _base_, parameters):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.trend = None
        self.global_market_sentiment = None
        self.local_market_sentiment = None
        self.parameters = parameters
        self.global_params = self.parameters.get('runtime_params.global_trade')
        self.market_indices = self.parameters.get('global_params.market_indices')
        self.market_sentiment = None

    def initialize(self):
        return self.analyze_market_sentiments()

    def get_local_market_sentiment(self):
        log_info("Analyzing local market sentiment ...COMPLETE!")
        return True if self.market_sentiment == Market_Sentiment.POSITIVE else False if self.market_sentiment == Market_Sentiment.NEGATIVE else None

    def get_global_market_sentiment(self):
        log_info("Analyzing global market sentiment ...COMPLETE!")
        return True if self.market_sentiment == Market_Sentiment.POSITIVE else False if self.market_sentiment == Market_Sentiment.NEGATIVE else None

    # Analyze market sentiment and determine strategy recommendations:
    def analyze_market_sentiments(self):
        if self.global_params:
            self.local_market_sentiment = self.get_local_market_sentiment()
            self.global_market_sentiment = self.get_global_market_sentiment()

        if self.local_market_sentiment and self.global_market_sentiment:
            self.trend = "Market Sentiment: Bullish"
        elif self.local_market_sentiment and not self.global_market_sentiment:
            self.trend = "Market Sentiment: Sideways"
        else:
            self.trend = "Market Sentiment: Bearish"

        log_info(f"{self.trend}")
        return self.trend

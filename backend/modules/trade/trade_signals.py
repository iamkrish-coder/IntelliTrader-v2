# TradeExecutionSignals
import time
from datetime import datetime, timedelta

from .BaseTrade import BaseTrade
from backend.constants.const import *
from backend.enumerations.enums import *
from ...controllers.BaseController import BaseController
from ...models.signals_model import SignalsModel
from backend.utils.logging_utils import *


class TradeSignals(BaseController, BaseTrade):
    def __init__(self, _base_, parameters, event, signals=None):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.event = event
        self.signals = signals

    def initialize(self):
        match self.event:
            case "get":
                return self.get_signals()

            case "post":
                return self.update_signals()

            case _:  # Default case
                log_warn(f"Unknown event type: {self.event}")

    def get_signals(self):
        try:
            dataset = None
            threshold_time = (datetime.datetime.now() - datetime.timedelta(minutes=300)).strftime('%Y-%m-%d %H:%M:%S') # 5 Minutes
            list_signals = self.prepare_request_parameters(
                event=Events.SCAN.value,
                table=Tables.TABLE_SIGNALS.value,
                model=None,
                dataset=dataset,
                projection=[
                    "signal_id",
                    "signal_strategy",
                    "signal_type",
                    "signal_exchange",
                    "signal_symbol",
                    "signal_token",
                    "created_date"],
                filters={
                    "is_active": True,
                    "is_complete": False,
                    "created_date": {'gte': threshold_time}
                }
            )
            signals = self.database.database_request(list_signals)
            return signals
        except Exception as error:
            log_info(f"An error occurred retrieving trade signals: {error}")
            return None

    def update_signals(self):
        try:
            self.signal_ids = [item['signal_id'] for item in self.signals]
            # Update the valid signals only
            for signal_id in self.signal_ids:
                # Add entry to AWS DynamoDB
                dataset = {
                    "signal_id": signal_id,
                    "is_complete": True,
                    "is_active": False
                }
                update_topics = self.prepare_request_parameters(
                    event=Events.UPDATE.value,
                    table=Tables.TABLE_SIGNALS.value,
                    model=SignalsModel,
                    dataset=dataset
                )
                self.database.database_request(update_topics)

        except Exception as error:
            log_info(f"An error occurred updating trade signals: {error}")
            return None
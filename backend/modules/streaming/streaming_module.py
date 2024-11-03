import datetime as dt
import time
from backend.utils.logging_utils import *


class Ticker:
    def __init__(self, params):
        self.mode = None
        self.exit_time = None
        self.entry_price = None
        self.target_profit = None
        self.stop_loss = None
        self.target_profit_points = None
        self.stop_loss_points = None
        self.prop = params
        self.tokens = []
        self.ticker_data = []

        # Callback for successful connection.

    def on_connect(self, ws, response):
        log_info(f"Successfully connected. Response: {response}")
        ticker_token = self.tokens
        ticker_mode = None
        ws.subscribe(ticker_token)

        if self.mode.lower() == "ltp":
            ticker_mode = ws.MODE_LTP
        elif self.mode.lower() == "quote":
            ticker_mode = ws.MODE_QUOTE
        elif self.mode.lower() == "full":
            ticker_mode = ws.MODE_FULL
        else:
            log_warn(f"No ticker mode is defined: {ticker_mode}")

        ws.set_mode(ticker_mode, ticker_token)
        log_info(f"Subscribe to tokens in Full/LTP/Quote mode: {ticker_token}")

    # Callback when current connection is closed.
    def on_close(self, ws, code, reason):
        log_info(f"Connection closed: {code} - {reason}")
        # Reconnection will not happen after executing `ws.stop()`
        # ws.stop()

    # Callback when connection closed with error.
    def on_error(self, ws, code, reason):
        log_info(f"Connection error: {code} - {reason}")

    # Callback when reconnect is on progress
    def on_reconnect(self, ws, attempts_count):
        log_info(f"Reconnecting: {attempts_count}")

    # Callback when all reconnect failed (exhausted max retries)
    def on_noreconnect(self, ws):
        log_info("Reconnect failed.")

    # Callback for tick reception.
    def on_ticks(self, ws, ticks):
        if len(ticks) > 0:
            #log_info(f"Current mode: {ticks[0]['mode']}")
            self.ticker_data.extend(ticks)
            self.process_ticker_data(ws)

    # Process the stored ticker data or perform any required operations
    def process_ticker_data(self, ws):
        begin_time = time.time()
        for tick in self.ticker_data:
            log_info(f"Ticks: {tick}")
            time.sleep(2)

            # if dt.datetime.now().time() >= self.exit_time:
            #     ws.stop()  # Close the connection at a specific time

            # target_profit = self.target_profit
            # if tick[-1]['last_price'] >= target_profit:
            #     ws.stop()  # Close the connection when target price is reached

            # stop_loss = self.stop_loss
            # if tick[-1]['last_price'] <= stop_loss:
            #     ws.stop()  # Close the connection when stop loss is triggered

            # entry_price = self.entry_price
            # target_profit_points = self.target_profit_points
            # if tick[-1]['last_price'] >= entry_price + target_profit_points:
            #     ws.stop()  # Close the connection when profit target is reached

            # if (time.time() - begin_time) > 120: # run for 2 minutes
            #     ws.close() # close the connection after some time

    def connect_to_ticker(self, tokens, mode, user_settings):
        self.tokens = tokens
        self.mode = mode
        self.exit_time = dt.time(15, 30)

        # Access user settings using dictionary keys
        self.entry_price = float(user_settings.get("en_price", 0))
        self.target_profit = float(user_settings.get("tp_price", 0))
        self.stop_loss = float(user_settings.get("sl_price", 0))
        self.target_profit_points = float(user_settings.get("tp_points", 0))
        self.stop_loss_points = float(user_settings.get("sl_points", 0))

        # Assign the callbacks    
        self.prop['kiteticker'].on_connect = self.on_connect
        self.prop['kiteticker'].on_reconnect = self.on_reconnect
        self.prop['kiteticker'].on_noreconnect = self.on_noreconnect
        self.prop['kiteticker'].on_ticks = self.on_ticks
        self.prop['kiteticker'].on_close = self.on_close
        self.prop['kiteticker'].on_error = self.on_error

        self.prop['kiteticker'].connect(threaded=True, disable_ssl_verification=True)

        while True:
            if self.prop['kiteticker'].is_connected():
                self.prop['kiteticker'].set_mode(self.mode, self.tokens)
                time.sleep(2)

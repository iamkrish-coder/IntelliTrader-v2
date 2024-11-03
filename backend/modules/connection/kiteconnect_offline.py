import os
import requests
import dateutil.parser

from backend.constants import *
from backend.enumerations.enums import *
from backend.enumerations.resource_string_enums import *


class KiteConnectOffline:
    """
    The `KiteConnectOffline` class provides a Python interface for interacting with Zerodha's Kite Connect API in an offline mode.
    It establishes a session with the API using an enctoken and offers methods to retrieve various market data, place orders,
    and manage positions.

    **Note:** This class simulates an offline mode by directly fetching data and does not involve real-time updates.
    """

    def __init__(self, enctoken):
        """
        Initializes a KiteConnectOffline instance.

        Args:
            enctoken (str): The user's enctoken for authentication.
        """
        self.headers = {"Authorization": f"enctoken {enctoken}"}
        self.session = requests.session()
        self.root_url = "https://api.kite.trade"
        self.session.get(self.root_url, headers=self.headers)

    def instruments(self, exchange=None):
        """
        Retrieves a list of instruments for the specified exchange or all exchanges.

        Args:
            exchange (str, optional): The exchange code (e.g., "NSE", "BSE"). Defaults to None (all exchanges).

        Returns:
            list: A list of dictionaries containing instrument details, including instrument token, exchange token,
                  tradingsymbol, name, last price, expiry (if applicable), strike (if applicable), tick size,
                  lot size, instrument type, segment, and exchange.
        """

        data = self.session.get(f"{self.root_url}/instruments", headers=self.headers).text.split("\n")
        Exchange = []
        for i in data[1:-1]:
            row = i.split(",")
            if exchange is None or exchange == row[11]:
                Exchange.append({'instrument_token': int(row[0]), 'exchange_token': row[1], 'tradingsymbol': row[2],
                                 'name': row[3][1:-1], 'last_price': float(row[4]),
                                 'expiry': dateutil.parser.parse(row[5]).date() if row[5] != "" else None,
                                 'strike': float(row[6]), 'tick_size': float(row[7]), 'lot_size': int(row[8]),
                                 'instrument_type': row[9], 'segment': row[10],
                                 'exchange': row[11]})
        return Exchange

    def quote(self, instruments):
        """
        Retrieves live quotes for the specified instruments.

        Args:
            instruments (str, comma-separated): A comma-separated string of instrument tokens for which to fetch quotes.

        Returns:
            dict: A dictionary containing the live quotes for the requested instruments. The structure of the returned
                  dictionary may vary depending on the Zerodha API response format.
        """

        data = self.session.get(f"{self.root_url}/quote", params={"i": instruments}, headers=self.headers).json()[
            "data"]
        return data

    def ltp(self, instruments):
        """
        Retrieves the last traded price (LTP) for the specified instruments.

        Args:
            instruments (str, comma-separated): A comma-separated string of instrument tokens for which to fetch LTP.

        Returns:
            dict: A dictionary containing the LTP for the requested instruments. The structure of the returned
                  dictionary may vary depending on the Zerodha API response format.
        """

        data = self.session.get(f"{self.root_url}/quote/ltp", params={"i": instruments}, headers=self.headers).json()[
            "data"]
        return data

    def ohlc(self, instruments):
        """
        Retrieves historical OHLC (Open, High, Low, Close) data for the specified instruments.

        Args:
            instruments (str, comma-separated): A comma-separated string of instrument tokens for which to fetch OHLC data.

        Returns:
            list: A list of dictionaries containing OHLC data for each instrument. The structure of the returned
                  dictionaries may vary depending on the Zerodha API response format.
        """

        data = self.session.get(f"{self.root_url}/quote/ohlc", params={"i": instruments}, headers=self.headers).json()[
            "data"]
        return data

    def historical_data(self, instrument_token, from_date, to_date, interval, continuous=False, oi=False):
        """
        Retrieves historical OHLC (Open, High, Low, Close) data for the specified instrument and interval.

        Args:
            instrument_token (int): The instrument token of the security.
            from_date (str): The start date (YYYY-MM-DD) for the historical data request.
            to_date (str): The end date (YYYY-MM-DD) for the historical data request.
            interval (str): The time interval for the data ("minute", "day", "3minute", etc.).
            continuous (bool, optional): Flag to request continuous data (includes weekends and holidays). Defaults to False.
            oi (bool, optional): Flag to include Open Interest data (if available for the instrument). Defaults to False.

        Returns:
            list: A list of dictionaries containing historical data for each time period within the specified interval.
                  Each dictionary contains the following keys:
                      - date (datetime.date): The date for the data point.
                      - open (float): The opening price.
                      - high (float): The highest price during the interval.
                      - low (float): The lowest price during the interval.
                      - close (float): The closing price.
                      - volume (int): The volume traded during the interval.
                      - oi (float, optional): The Open Interest (if requested and available).
        """

        params = {"from": from_date,
                  "to": to_date,
                  "interval": interval,
                  "continuous": 1 if continuous else 0,
                  "oi": 1 if oi else 0}
        lst = self.session.get(
            f"{self.root_url}/instruments/historical/{instrument_token}/{interval}", params=params,
            headers=self.headers).json()["data"]["candles"]
        records = []
        for i in lst:
            record = {"date": dateutil.parser.parse(i[0]), "open": i[1], "high": i[2], "low": i[3],
                      "close": i[4], "volume": i[5], }
            if len(i) == 7:
                record["oi"] = i[6]
            records.append(record)
        return records

    def margins(self):
        """
        Retrieves user margins information from Zerodha.

        Returns:
            dict: A dictionary containing user margin details. The structure of the returned dictionary
                  may vary depending on the Zerodha API response format.
        """

        margins = self.session.get(f"{self.root_url}/user/margins", headers=self.headers).json()["data"]
        return margins

    def orders(self):
        """
        Retrieves a list of all open orders for the user.

        Returns:
            list: A list of dictionaries containing details of open orders. The structure of the returned
                    dictionaries may vary depending on the Zerodha API response format.
        """

        orders = self.session.get(f"{self.root_url}/orders", headers=self.headers).json()["data"]
        return orders

    def positions(self):
        """
        Retrieves a list of the user's current holdings (positions).

        Returns:
            list: A list of dictionaries containing details of user positions. The structure of the returned
                  dictionaries may vary depending on the Zerodha API response format.
        """

        positions = self.session.get(f"{self.root_url}/portfolio/positions", headers=self.headers).json()["data"]
        return positions

    def place_order(self, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price=None,
                    validity=None, disclosed_quantity=None, trigger_price=None, squareoff=None, stoploss=None,
                    trailing_stoploss=None, tag=None):
        """
        Places an order on Zerodha's Kite Connect platform.

        Args:
            variety (str): The order variety ("regular", "amo", or "co").
            exchange (str): The exchange code (e.g., "NSE", "BSE").
            tradingsymbol (str): The tradingsymbol of the instrument.
            transaction_type (str): The transaction type ("BUY" or "SELL").
            quantity (int): The quantity of the instrument to be traded.
            product (str): The product type (e.g., "MIS", "CNC", "NRML").
            order_type (str): The order type (e.g., "MARKET", "LIMIT", "SL-M", "SL", etc.).
            price (float, optional): The price for limit orders. Defaults to None.
            validity (str, optional): The order validity ("DAY", "IOC", etc.). Defaults to None.
            disclosed_quantity (int, optional): The disclosed quantity for iceberg orders. Defaults to None.
            trigger_price (float, optional): The trigger price for stop-loss market (SL-M) orders. Defaults to None.
            squareoff (float, optional): The square-off value for trailing stoploss orders. Defaults to None.
            stoploss (float, optional): The stop-loss value for stop-loss orders (SL and SL-M). Defaults to None.
            trailing_stoploss (float, optional): The trailing stoploss value. Defaults to None.
            tag (str, optional): A user-defined tag for the order. Defaults to None.

        Returns:
            int: The order ID of the placed order.
        """

        params = locals()
        del params["self"]
        for k in list(params.keys()):
            if params[k] is None:
                del params[k]
        order_id = self.session.post(f"{self.root_url}/orders/{variety}",
                                     data=params, headers=self.headers).json()["data"]["order_id"]
        return order_id

    def modify_order(self, variety, order_id, parent_order_id=None, quantity=None, price=None, order_type=None,
                     trigger_price=None, validity=None, disclosed_quantity=None):
        """
        Modifies an existing order on Zerodha's Kite Connect platform.

        Args:
            variety (str): The order variety ("regular", "amo", or "co").
            order_id (int): The ID of the order to be modified.
            parent_order_id (int, optional): The parent order ID for basket orders. Defaults to None.
            quantity (int, optional): The new quantity for the order. Defaults to None.
            price (float, optional): The new price for limit orders. Defaults to None.
            order_type (str, optional): The new order type. Defaults to None.
            trigger_price (float, optional): The new trigger price for SL-M orders. Defaults to None.
            validity (str, optional): The new order validity. Defaults to None.
            disclosed_quantity (int, optional): The new disclosed quantity for iceberg orders. Defaults to None.

        Returns:
            int: The order ID of the modified order (same as the original order ID).
        """

        params = locals()
        del params["self"]
        for k in list(params.keys()):
            if params[k] is None:
                del params[k]

        order_id = self.session.put(f"{self.root_url}/orders/{variety}/{order_id}",
                                    data=params, headers=self.headers).json()["data"][
            "order_id"]
        return order_id

    def cancel_order(self, variety, order_id, parent_order_id=None):
        """
        Cancels an existing order on Zerodha's Kite Connect platform.

        Args:
            variety (str): The order variety ("regular", "amo", or "co").
            order_id (int): The ID of the order
            
        Returns:
            int: The order ID of the cancelled order (same as the original order ID).            
        """

        order_id = self.session.delete(f"{self.root_url}/orders/{variety}/{order_id}",
                                       data={"parent_order_id": parent_order_id} if parent_order_id else {},
                                       headers=self.headers).json()["data"]["order_id"]
        return order_id

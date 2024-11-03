# TradeOrders
import time
import uuid

from backend.constants.const import *
from backend.enumerations.enums import *
from ...controllers.BaseController import BaseController
from ...models.trades_model import TradesModel
from backend.utils.logging_utils import *
from .BaseTrade import BaseTrade
from .trade_execute import ExecuteTrade
from ..orders.orders_module import Orders


class TradeOrders(BaseController, BaseTrade):
    def __init__(self, _base_, parameters, signals):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.signals = signals

    def initialize(self):
        self.execute_trade_order()

    def execute_trade_order(self):
        """ Execute Order """
        placed_orders = []
        orders = self.prepare_order_placement()
        if not orders:
            log_error("Error: Could not generate orders.")
            return

        for order in orders:
            try:
                object_execute_trade = ExecuteTrade(self.modules,
                                           order['variety'],
                                           order['exchange'],
                                           order['tradingsymbol'],
                                           order['transaction_type'],
                                           order['quantity'],
                                           order['disclosed_quantity'],
                                           order['order_type'],
                                           order['product'],
                                           order['price'],
                                           order['trigger_price'],
                                           order['validity'],
                                           order['validity_ttl'],
                                           order['iceberg_legs'],
                                           order['iceberg_quantity'],
                                           order['tag'])

                order['order_id'] = trade_order_response = object_execute_trade.execute_trade()
                if trade_order_response:
                    log_info(f"Order placed for {order['tradingsymbol']}: {trade_order_response}")

                    """" Save order summary to Trade History Table """
                    self.save_trade_history(order['tradingsymbol'], order['signal'], order['strategy'], order['order_id'])
                    time.sleep(1)
                else:
                    log_error(f"Failed to place order for {order['tradingsymbol']}")

            except Exception as error:
                log_error(f"Error placing order for {order['tradingsymbol']}: {error}")

        return placed_orders

    def save_trade_history(self, symbol, signal, strategy, order_id):

        trade_id = self.generate_table_uid(TABLE_TRADES)
        dataset = {
            "trade_id": trade_id,
            "trade_signal_id": signal,
            "trade_strategy": strategy,
            "trade_order_id": order_id,
            "trade_symbol": symbol,
            "created_date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        save_trade_order_history = self.prepare_request_parameters(
            event=Events.PUT.value,
            table=Tables.TABLE_TRADES.value,
            model=TradesModel,
            dataset=dataset
        )
        self.database_request(save_trade_order_history)

    def prepare_order_placement(self):
        """ Prepare Order Pre-requisites and parameters """
        """"
        variety 	
            regular Regular order
            amo 	After Market Order
            co 	    Cover Order 
            iceberg Iceberg Order 
            auction Auction Order 
        order_type 	
            MARKET 	Market order
            LIMIT 	Limit order
            SL 	    Stoploss order 
            SL-M 	Stoploss-market order 
        product 	
            CNC 	Cash & Carry for equity 
            NRML 	Normal for futures and options 
            MIS 	Margin Intraday Squareoff for futures and options 
        validity 	
            DAY 	Regular order
            IOC 	Immediate or Cancel
            TTL 	Order validity in minutes
        """

        trade_order_parameters = []
        for signal in self.signals:

            order_params = {}

            # Signal information
            signal_id = signal['signal_id']
            signal_strategy = signal['signal_strategy']
            signal_token = signal['signal_token']
            strategy_type = int(self.parameters.get('strategy_params.strategy_type'))
            signal_exchange = int(signal['signal_exchange'])
            signal_symbol = signal['signal_symbol']
            signal_transaction_type = int(signal['signal_type'])

            instrument = self.parameters.get('strategy_params.instrument')
            if instrument == Instrument_Type.EQUITY.value:
                trade_parameters = self.parameters.get('strategy_params.equity_trade_params')
            elif instrument == Instrument_Type.OPTIONS.value:
                trade_parameters = self.parameters.get('strategy_params.options_trade_params')
            elif instrument == Instrument_Type.FUTURES.value:
                trade_parameters = self.parameters.get('strategy_params.futures_trade_params')
            else:
                log_error("No instrument trade type defined in the configuration.")
                return False

            # Caclulate Quantity
            lot_size = self.modules['fetch'].instrument_lot_size_lookup(signal_exchange, signal_symbol)
            max_quantity = int(trade_parameters.get('max_quantity'))
            position_size_type = int(trade_parameters.get('position_size_type'))
            max_allocation = float(trade_parameters.get('max_allocation'))
            max_risk = float(trade_parameters.get('max_risk'))
            quantity = self.set_quantity(signal_exchange, signal_symbol, max_quantity, position_size_type, max_allocation, max_risk, lot_size)

            if quantity == 0:
                log_warn(f"Insufficient margin. Please add funds to proceed.")
                return None

            # Calculate Price for Limit/SL/SL-M/GTT
            price = 0
            trigger_price = 0
            order_type = int(trade_parameters.get('order_type'))
            default_price = int(trade_parameters.get('default_price'))
            limit_buffer = float(trade_parameters.get('buffer'))

            if order_type == Order_Type.LIMIT.value:
                price = self.set_limit_price(signal_exchange, signal_symbol, default_price, limit_buffer)
                if price < 0:
                    log_error(f"Limit buffer must not exceed stock trading price.")
                    return None

            if order_type == Order_Type.SL.value or order_type == Order_Type.SL_M.value:
                # TODO: Awaits Implementation
                trigger_price = self.set_trigger_price()

            if order_type == Order_Type.GTT.value:
                # TODO: Awaits Implementation
                pass

            # Others
            product = int(trade_parameters.get('product'))
            if not self.validate_product(instrument, product):
                return False

            validity = int(trade_parameters.get('validity'))
            validity_ttl = int(trade_parameters.get('validity_ttl'))
            variety = int(trade_parameters.get('variety'))
            iceberg_legs = int(trade_parameters.get('iceberg_legs'))
            iceberg_quantity = int(trade_parameters.get('iceberg_quantity'))
            disclosed_quantity = int(trade_parameters.get('disclosed_quantity'))
            tag = trade_parameters.get('tag')

            """ BUILD ORDER PARAMETERS DICTIONARY """
            order_parameters = {
                "signal": signal_id,
                "strategy":  signal_strategy,
                "variety": variety,
                "exchange": signal_exchange,
                "tradingsymbol": signal_symbol,
                "transaction_type": signal_transaction_type,
                "quantity": quantity,
                "disclosed_quantity": disclosed_quantity,
                "order_type": order_type,
                "product": product,
                "price": price,
                "trigger_price": trigger_price,
                "validity": validity,
                "validity_ttl": validity_ttl,
                "iceberg_legs": iceberg_legs,
                "iceberg_quantity": iceberg_quantity,
                "tag": tag
            }
            trade_order_parameters.append(order_parameters)
        return trade_order_parameters

    def validate_product(self, instrument, product):
        allowed_products = {
            Instrument_Type.EQUITY: [Product.MIS.value, Product.CNC.value],
            Instrument_Type.OPTIONS: [Product.MIS.value, Product.NRML.value],
            Instrument_Type.FUTURES: [Product.MIS.value, Product.NRML.value]
        }

        instrument_enum = Instrument_Type(instrument)
        if instrument_enum not in allowed_products or product not in allowed_products[instrument_enum]:
            log_error(f"Invalid Product for {instrument_enum.name}. Allowed products: {allowed_products[instrument_enum]}")
            return False
        else:
            return True

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class CreateMarketOrder:
    def __init__(self, order_parameters, prop):
        self.order_parameters = order_parameters
        self.prop = prop

    def initialize(self):
        return self.create_market_order()

    # Place a market order for a stock with given quantity
    def create_market_order(self):

        trade_variety, trade_exchange, trade_symbol, trade_transaction_type, trade_quantity, trade_disclosed_quantity, trade_ordertype, trade_product, trade_price, trade_trigger_price, trade_validity, trade_validity_ttl, trade_iceberg_legs, trade_iceberg_quantity, trade_tag = self.order_parameters

        # Define mapping dictionaries for each parameter
        variety_mapping = {
            Variety.REGULAR.value: VARIETY_REGULAR,
            Variety.AMO.value: VARIETY_AMO,
            Variety.CO.value: VARIETY_CO,
            Variety.ICEBERG.value: VARIETY_ICEBERG,
            Variety.AUCTION.value: VARIETY_AUCTION
        }

        exchange_mapping = {
            Exchange.NSE.value: EXCHANGE_NSE,
            Exchange.BSE.value: EXCHANGE_BSE,
            Exchange.NFO.value: EXCHANGE_NFO
        }

        transaction_mapping = {
            Transaction_Type.BUY.value: TRANSACTION_TYPE_BUY,
            Transaction_Type.SELL.value: TRANSACTION_TYPE_SELL
        }

        product_mapping = {
            Product.CNC.value: PRODUCT_CNC,
            Product.NRML.value: PRODUCT_NRML,
            Product.MIS.value: PRODUCT_MIS
        }

        order_type_mapping = {
            Order_Type.MARKET.value: ORDER_TYPE_MARKET,
            Order_Type.LIMIT.value: ORDER_TYPE_LIMIT,
            Order_Type.SL.value: ORDER_TYPE_SL,
            Order_Type.SL_M.value: ORDER_TYPE_SLM
        }

        validity_mapping = {
            Validity.DAY.value: VALIDITY_DAY,
            Validity.IOC.value: VALIDITY_IOC,
            Validity.TTL.value: VALIDITY_TTL,
        }

        # Convert strings to constants using the mapping dictionaries
        trade_variety = variety_mapping.get(trade_variety)
        trade_exchange = exchange_mapping.get(trade_exchange)
        trade_transaction_type = transaction_mapping.get(trade_transaction_type)
        trade_product = product_mapping.get(trade_product)
        trade_ordertype = order_type_mapping.get(trade_ordertype)
        trade_validity = validity_mapping.get(trade_validity)

        if trade_variety is None:
            log_error("The order placement does not have a specified variety to Regular, AMO, CO, Iceberg, or Auction.")
            return False

        if trade_exchange is None:
            log_error("The order placement does not have a specified exchange to NSE or BSE.")
            return False

        if trade_transaction_type is None:
            log_error("The order placement does not have a specified action to buy or sell.")
            return False

        if trade_product is None:
            log_error("The order placement does not have a specified product to MIS, CNC, or NRML.")
            return False

        if trade_ordertype is None:
            log_error("The order type does not match the required format.")
            return False

        try:
            order_id = self.prop['kite'].place_order(
                variety=trade_variety,
                exchange=trade_exchange,
                tradingsymbol=trade_symbol,
                transaction_type=trade_transaction_type,
                quantity=trade_quantity,
                disclosed_quantity=trade_disclosed_quantity,
                product=trade_product,
                order_type=trade_ordertype,
                price=trade_price,
                trigger_price=trade_trigger_price,
                validity=trade_validity,
                validity_ttl=trade_validity_ttl,
                iceberg_legs=trade_iceberg_legs,
                iceberg_quantity=trade_iceberg_quantity,
                tag=trade_tag
            )

            log_info(f"Market order placed. Order ID: {order_id}")
            return order_id

        except Exception as error:
            log_info("Order placement failure: {}".format(error))


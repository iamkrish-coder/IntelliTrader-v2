from .BaseTrade import BaseTrade


class ExecuteTrade(BaseTrade):
    def __init__(self, modules, variety, exchange, tradingsymbol, transaction_type, quantity, disclosed_quantity, order_type, product,  price, trigger_price, validity, validity_ttl, iceberg_legs, iceberg_quantity, tag):
        super().__init__(modules, transaction_type, order_type)
        self.variety = variety
        self.exchange = exchange
        self.tradingsymbol = tradingsymbol
        self.quantity = quantity
        self.disclosed_quantity = disclosed_quantity
        self.product = product
        self.price = price
        self.trigger_price = trigger_price
        self.validity = validity
        self.validity_ttl = validity_ttl
        self.iceberg_legs = iceberg_legs
        self.iceberg_quantity = iceberg_quantity
        self.tag = tag

    def buy(self):
        order_parameters = [self.variety, self.exchange, self.tradingsymbol, self.transaction_type, self.quantity, self.disclosed_quantity, self.order_type, self.product, self.price, self.trigger_price, self.validity, self.validity_ttl, self.iceberg_legs, self.iceberg_quantity, self.tag]
        return self.create_trade_order(order_parameters)

    def sell(self):
        order_parameters = [self.variety, self.exchange, self.tradingsymbol, self.transaction_type, self.quantity, self.disclosed_quantity, self.order_type, self.product, self.price, self.trigger_price, self.validity, self.validity_ttl, self.iceberg_legs, self.iceberg_quantity, self.tag]
        return self.create_trade_order(order_parameters)

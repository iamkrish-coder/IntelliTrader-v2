# handlers/strategy
from asyncio import current_task

import numpy as np
import pandas as pd

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.logging_utils import *
from ...controllers.BaseController import BaseController
from .BaseStrategy import BaseStrategy


class StrategyWatchlist(BaseController, BaseStrategy):
    def __init__(self, _base_, parameters):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.exchange = self.parameters.get('strategy_params.exchange')
        self.symbol = self.parameters.get('strategy_params.symbol')

    def initialize(self):
        return self.get_stock_watchlist()

    def get_stock_basket(self, exchange, symbol):
        stock_basket = []
        if exchange.upper() == EXCHANGE_NSE or exchange.upper() == EXCHANGE_BSE or exchange.upper() == EXCHANGE_NFO:
            if symbol.upper() == "EQUITY":
                symbols_list = pd.read_csv(EQUITY_BASKET)
                stock_basket = symbols_list['Symbol'].tolist()
            elif symbol.upper() == "INDEX-OPTIONS":
                symbols_list = pd.read_csv(INDEX_OPTIONS_BASKET)
                stock_basket = symbols_list['Symbol'].tolist()
            elif symbol.upper() == "STOCK-OPTIONS":
                symbols_list = pd.read_csv(STOCK_OPTIONS_BASKET)
                stock_basket = symbols_list['Symbol'].tolist()
            elif symbol.upper() == "FUTURES":
                symbols_list = pd.read_csv(FUTURES_BASKET)
                stock_basket = symbols_list['Symbol'].tolist()
            else:
                stock_basket.append(symbol.upper())

        else:
            log_info(f"Invalid Exchange {exchange}")
        return stock_basket

    def get_stock_watchlist(self):
        stock_basket = self.get_stock_basket(self.exchange, self.symbol)
        instruments_list = self.modules['fetch'].fetch_instruments(self.exchange)

        if self.symbol.upper() == "INDEX-OPTIONS" or self.symbol.upper() == "STOCK-OPTIONS":
            watchlist_stocks_dataframe = self.get_option_chain_contracts(instruments_list, stock_basket)
            watchlist_stocks = watchlist_stocks_dataframe.to_dict('records')
        elif self.symbol.upper() == "FUTURES":
            # future_chain = self.extract_futures(instruments_list, stock_basket)
            pass
        else:
            watchlist_stocks = [instrument for instrument in instruments_list if instrument['tradingsymbol'] in stock_basket]

        return watchlist_stocks


    def get_option_chain_contracts(self, instruments_list, stock_basket):

        contracts = []
        option_chain_data = []
        option_chain_data_list = []

        option_instrument_type = self.parameters['strategy_params.option_instrument_type']
        if option_instrument_type == Option_Type.CE.value:
            option_type = FO_CE
        elif option_instrument_type == Option_Type.PE.value:
            option_type = FO_PE
        else:
            option_type = [FO_CE, FO_PE]

        for instrument in instruments_list:
            if (instrument['name'] in stock_basket or instrument['tradingsymbol'] in stock_basket) and instrument['instrument_type'] in option_type:
                contracts.append(instrument)

        option_contracts = pd.DataFrame(contracts)

        expiry_span = self.parameters['strategy_params.option_expiry_span']
        strike_span = self.parameters['strategy_params.option_strike_span']

        for stock in stock_basket:
            instrument_type = self.symbol.upper()
            underlying_price = self.get_underlying_price(instrument_type, stock)
            ce_contracts, pe_contracts = self.get_ce_pe_with_expiry(option_contracts, expiry_span, option_instrument_type, stock)

            if not ce_contracts.empty and not pe_contracts.empty and underlying_price is not None:
                option_chain_data = pd.concat([
                    self.get_call_option_chain(ce_contracts, underlying_price, strike_span),
                    self.get_put_option_chain(pe_contracts, underlying_price, strike_span)
                ], ignore_index=True)
            elif not ce_contracts.empty:
                option_chain_data = self.get_call_option_chain(ce_contracts, underlying_price, strike_span)
            elif not pe_contracts.empty:
                option_chain_data = self.get_put_option_chain(pe_contracts, underlying_price, strike_span)
            else:
                option_chain_data = pd.DataFrame()
                log_error(f"No option chain contracts found for {stock}")
                continue

            option_chain_data_list.append(option_chain_data)

        option_chain_data = pd.concat(option_chain_data_list, ignore_index=True)
        return option_chain_data


    def get_underlying_price(self, instrument_basket_type, instrument):
        symbol = None
        exchange = EXCHANGE_NFO

        if instrument_basket_type.upper() == "INDEX-OPTIONS":
            if instrument == "NIFTY":
                symbol = "NIFTY 50"
                exchange = EXCHANGE_NSE  # override NFO to NSE as these are Indices
            elif instrument == "BANKNIFTY":
                symbol = "NIFTY BANK"
                exchange = EXCHANGE_NSE  # override NFO to NSE as these are Indices
            elif instrument == "FINNIFTY":
                symbol = "NIFTY FIN SERVICE"
                exchange = EXCHANGE_NSE  # override NFO to NSE as these are Indices
            else:
                log_error(f"Instrument {instrument} is not available for an Index Option Trading")
                return
        elif instrument_basket_type.upper() == "STOCK-OPTIONS":
            symbol = instrument
            exchange = EXCHANGE_NSE
        else:
            log_error(f"Instrument {instrument} is not valid for an Index or Stock derivative Trading")

        if symbol is not None and exchange is not None:
            instrument_quote = self.modules['fetch'].fetch_quote(exchange, symbol)

            if instrument_quote is not None and instrument_quote != {}:
                for key in instrument_quote.keys():
                    symbol_key = key
                    last_price = instrument_quote[symbol_key]['last_price']
                    return last_price
            else:
                log_error(f"Instrument Quote not available for {exchange}:{symbol}")
        else:
            log_error(f"Instrument does not contain a valid underlying")


    def get_ce_pe_with_expiry(self, contracts, expiry_span, option_type, stock):

        contracts['time_to_expiry'] = (pd.to_datetime(contracts['expiry']) + datetime.timedelta(0,24*3600) - datetime.datetime.now()).dt.days
        contracts_filtered = contracts[contracts['name'] == stock]

        if not contracts_filtered.empty:
            next_expiry_in_days = np.sort(contracts_filtered['time_to_expiry'].unique())

            if next_expiry_in_days is not []:
                if expiry_span <= len(next_expiry_in_days):
                    expiry_eta = next_expiry_in_days[expiry_span]

                    if option_type == Option_Type.CE.value:
                        ce_contracts = contracts_filtered[(contracts_filtered['instrument_type'] == Option_Type.CE.name) & (contracts_filtered['time_to_expiry'] == expiry_eta)]
                        pe_contracts = pd.DataFrame()
                    elif option_type == Option_Type.PE.value:
                        ce_contracts = pd.DataFrame()
                        pe_contracts = contracts_filtered[(contracts_filtered['instrument_type'] == Option_Type.PE.name) & (contracts_filtered['time_to_expiry'] == expiry_eta)]
                    else:
                        ce_contracts = contracts_filtered[(contracts_filtered['instrument_type'] == Option_Type.CE.name) & (contracts_filtered['time_to_expiry'] == expiry_eta)]
                        pe_contracts = contracts_filtered[(contracts_filtered['instrument_type'] == Option_Type.PE.name) & (contracts_filtered['time_to_expiry'] == expiry_eta)]
                else:
                    ce_contracts = pd.DataFrame()
                    pe_contracts = pd.DataFrame()
        else:
            ce_contracts = pd.DataFrame()
            pe_contracts = pd.DataFrame()

        return ce_contracts.reset_index(drop=True), pe_contracts.reset_index(drop=True)


    def get_call_option_chain(self, contracts, current_index_price, strike_span):
        contracts.sort_values(by=['strike'], inplace=True, ignore_index=True)
        atm_index = (abs(contracts['strike'] - current_index_price).argmin()) + 1
        return contracts.iloc[atm_index - strike_span:atm_index].reset_index(drop=True)


    def get_put_option_chain(self, contracts, current_index_price, strike_span):
        contracts.sort_values(by=['strike'], inplace=True, ignore_index=True)
        atm_index = (abs(contracts['strike'] - current_index_price).argmin()) + 1
        return contracts.iloc[atm_index:atm_index + strike_span].reset_index(drop=True)



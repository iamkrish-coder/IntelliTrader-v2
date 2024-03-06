import os
import logging
import pandas as pd
import datetime as dt
import source.libraries.nse_data_api as _nseData
import source.libraries.market_durations_api as _marketDurations
import requests
import calendar
from turtle import st
from source.helper import Helper
from tkinter.tix import COLUMN
from source.constants.constants import *
from concurrent.futures import ProcessPoolExecutor
from functools import partial

class Fetch:
    def __init__(self, params):
        self.prop = params

    # Fetch instruments list
    def fetch_instruments(self, exchange=None):
        instruments_dump = self.prop['kite'].instruments(exchange)
        if exchange is not None:
            Helper().write_csv_output(f'instruments_{exchange}.csv', instruments_dump)
        else:
            Helper().write_csv_output('instruments.csv', instruments_dump)
        return instruments_dump

    # Lookup instrument token 
    def instrument_token_lookup(self, exchange, symbol):
        if exchange and symbol:
            nse_instruments_dump = self.prop['kite'].instruments(exchange)
            instrument_df = pd.DataFrame(nse_instruments_dump)
            try:
                instrument_token = instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]
                logging.info(f'::::::: Instrument ::::::: Exchange: {exchange} Symbol: {symbol} Token: {instrument_token} ...COMPLETE!')
                return instrument_token
            except Exception as e:
                logging.warning(f"An exception occurred: {e}")
                exit()
        else:
            logging.warning(f'Please verify that the exchange {exchange} and symbol {symbol} are present.')
            exit()

    # Lookup instrument token list (web streaming)
    def stream_instrument_token_lookup(self, exchange, symbol_list):
        if exchange and symbol_list:
            nse_instruments_dump = self.prop['kite'].instruments(exchange)
            instrument_df = pd.DataFrame(nse_instruments_dump)
            token_list = []
            
            try:
                for symbol in symbol_list:
                    token_list.append(int(instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]))
                return token_list
            except Exception as e:
                logging.warning(f"An exception occurred: {e}")
                exit()
        else:
            logging.warning(f'Please verify that the exchange [{exchange}] and symbol_list [{symbol_list}] are present.')
            exit()
            
    # Fetch historical data for an exchange and symbol    
    def fetch_ohlc(self, exchange, symbol, token, timeframe='5minute', depth=2):

        duration_obj = _marketDurations.MarketDurations(depth)
        duration = duration_obj.calculate_all_durations()
        
        if token:
            instrument_token = token
        else:    
            instrument_token = self.instrument_token_lookup(exchange, symbol)
        
        data = pd.DataFrame()
        if exchange and symbol and instrument_token and timeframe and duration:
            
            if timeframe.__contains__('today'):
                
                # Fetch Minutes Data
                duration = duration['today']
                
                if 'today1minute' in timeframe:
                    timeframe = 'minute'
                    timeframe_text = 'Today 1MINUTE'
                elif 'today2minute' in timeframe:
                    timeframe = '2minute'      
                    timeframe_text = 'Today 2MINUTE'                    
                elif 'today3minute' in timeframe:
                    timeframe = '3minute'
                    timeframe_text = 'Today 3MINUTE'                    
                elif 'today5minute' in timeframe:
                    timeframe = '5minute'  
                    timeframe_text = 'Today 5MINUTE'                    
                elif 'today15minute' in timeframe:    
                    timeframe = '15minute'
                    timeframe_text = 'Today 15MINUTE'                    
                elif 'today30minute' in timeframe:    
                    timeframe = '30minute'
                    timeframe_text = 'Today 30MINUTE'                    
                elif 'today60minute' in timeframe:    
                    timeframe = '60minute'
                    timeframe_text = 'Today 60MINUTE'                    
                else:
                    logging.error(f"No valid timeframe for exchange:symbol {exchange}:{symbol}")
                    return None
                
                data = pd.DataFrame(self.prop['kite'].historical_data(instrument_token, dt.date.today()-dt.timedelta(duration), dt.date.today(), timeframe)) 
                
                current_time = dt.datetime.now().time()
                if current_time >= dt.time(0, 0) and current_time < dt.time(9, 15):
                    pass
                else:            
                    data['date'] = pd.to_datetime(data['date'])
                    today_date = dt.datetime.now().date()
                    data = data[data['date'].dt.date == today_date]
                logging.info(f'::::::: OHLCV ::::::: Timeframe: {timeframe_text.upper()} Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')
                
            elif timeframe.__contains__('minute'):
                # Fetch Minutes Data
                duration = duration['minute']
                data = pd.DataFrame(self.prop['kite'].historical_data(instrument_token, dt.date.today()-dt.timedelta(duration), dt.date.today(), timeframe)) 
                logging.info(f'::::::: OHLCV ::::::: Timeframe: {timeframe.upper()} Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')
            
            elif timeframe.__contains__('hour'):
                # Fetch Hours Data
                duration = duration['hour']               
                data = pd.DataFrame(self.prop['kite'].historical_data(instrument_token, dt.date.today()-dt.timedelta(duration), dt.date.today(), timeframe)) 
                logging.info(f'::::::: OHLCV ::::::: Timeframe: {timeframe.upper()} Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')

            elif timeframe.__contains__('day'):
                # Fetch Daily Data
                duration = duration['day']                              
                data = pd.DataFrame(self.prop['kite'].historical_data(instrument_token, dt.date.today()-dt.timedelta(duration), dt.date.today(), timeframe))   
                logging.info(f'::::::: OHLCV ::::::: Timeframe: {timeframe.upper()} Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')

            elif timeframe.__contains__('week'):
                # Fetch Weekly Data
                timeframe = 'day'
                duration = duration['week']                                              
                data = pd.DataFrame(self.prop['kite'].historical_data(instrument_token, dt.date.today()-dt.timedelta(duration), dt.date.today(), timeframe))    
                data = self.aggregate_to_weekly(data)
                logging.info(f'::::::: OHLCV ::::::: Timeframe: {timeframe.upper()} Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')
                    
            elif timeframe.__contains__('month'):
                # Fetch Monthly Data
                timeframe = 'day'
                duration = duration['month']                                                             
                data = pd.DataFrame(self.prop['kite'].historical_data(instrument_token, dt.date.today()-dt.timedelta(duration), dt.date.today(), timeframe))   
                data = self.aggregate_to_monthly(data)
                logging.info(f'::::::: OHLCV ::::::: Timeframe: {timeframe.upper()} Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')
                    
            else:
                data = None
            
            if data is None or data.empty:
                logging.warning(f"No data found for exchange:symbol {exchange}:{symbol}")
                return None
            else:    
                Helper().write_csv_output(f'historical_{exchange}_{symbol}.csv', data)
                return data
        else:
            logging.warning(f'Please verify that the exchange [{exchange}], symbol [{symbol}], timeframe[{timeframe}] and duration[{duration}] are present.')
            return None

    def aggregate_to_weekly(self, daily_data):      
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        daily_data.set_index('date', inplace=True)

        if not isinstance(daily_data.index, pd.DatetimeIndex):
            daily_data.index = pd.to_datetime(daily_data.index)

        # Resample the daily data to weekly OHLC data
        weekly_data = daily_data.resample('W').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        return weekly_data

    def aggregate_to_monthly(self, daily_data):
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        daily_data.set_index('date', inplace=True)

        if not isinstance(daily_data.index, pd.DatetimeIndex):
            daily_data.index = pd.to_datetime(daily_data.index)

        # Resample the daily data to monthly OHLC data
        monthly_data = daily_data.resample('M').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        return monthly_data


    # Fetch extended historical data for an exchange and symbol with limits   
    def fetch_ohlc_extended(self, exchange, symbol, timeframe, duration=1):
        if exchange and symbol and timeframe and duration:
            instrument_token = self.instrument_token_lookup(exchange, symbol)
            match timeframe:
                case "minute":
                    lookback_period_threshold = 60
                case "3minute":
                    lookback_period_threshold = 100
                case "5minute":
                    lookback_period_threshold = 100
                case "10minute":
                    lookback_period_threshold = 100
                case "15minute":
                    lookback_period_threshold = 200
                case "30minute":
                    lookback_period_threshold = 200
                case "60minute":
                    lookback_period_threshold = 400
                case "day":
                    lookback_period_threshold = 2000
                case _:
                    lookback_period_threshold = 1

            start_date = dt.date.today()-dt.timedelta(duration)
            end_date = dt.date.today()
            
            data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            while True:
                if start_date.date() >= (end_date - dt.timedelta(lookback_period_threshold)):
                    data = data._append(pd.DataFrame(self.prop['kite'].historical_data(instrument_token, start_date, end_date, timeframe)), ignore_index=True)
                    break
                else:
                    end_date = start_date + dt.timedelta(lookback_period_threshold)
                    data = data._append(pd.DataFrame(self.prop['kite'].historical_data(instrument_token, start_date, end_date, timeframe)), ignore_index=True)
                    start_date = end_date
    
            Helper().write_csv_output(f'historical_{exchange}_{symbol}_{lookback_period_threshold}.csv', data)
            logging.info(f'::::::: OHLCV ::::::: Timeframe: {timeframe} Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')
            return data
        else:
            logging.warning(f'Please verify that the exchange [{exchange}], symbol [{symbol}], start_date[{start_date}] and timeframe[{timeframe}] are present.')
            exit()

    # Fetch quote
    def fetch_quote(self, exchange, symbol):
        if exchange and symbol:
            quote = self.prop['kite'].quote(f'{exchange}:{symbol}')
            logging.info(f'::::::: Quote ::::::: Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')          
            return quote
        else:
            logging.warning(f'Please verify that the exchange [{exchange}] and symbol [{symbol}] are present.')
            exit()

    # Fetch ltp 
    def fetch_ltp(self, exchange, symbol):
        if exchange and symbol:
            last_traded_price = self.prop['kite'].ltp(f'{exchange}:{symbol}')
            logging.info(f'::::::: LTP ::::::: Exchange: {exchange} Symbol: {symbol} ...COMPLETE!')                     
            return last_traded_price
        else:
            logging.warning(f'Please verify that the exchange [{exchange}] and symbol [{symbol}] are present.')
            exit()

    # Fetch orders 
    def fetch_orders(self):
        orders = self.prop['kite'].orders()
        return orders

    # Fetch positions 
    def fetch_positions(self):
        positions = self.prop['kite'].positions()
        return positions

    # Fetch holdings
    def fetch_holdings(self):
        holdings = self.prop['kite'].holdings()
        return holdings

    # --------------------------------------------------------------------------------------
        # BACKTESTING - FUTURE PURPOSE ONLY
    # --------------------------------------------------------------------------------------

    # Fetch backtest data
    def fetch_backtest_data(self, args):        
        if(args['backtest_timeframe'] == 'latest'):
            return(self.fetch_backtest_latest_data(_nseData, args))
        else:
            return(self.fetch_backtest_historical_data(args))
                
    def fetch_backtest_latest_data(_nseData, dataset):
        # Check if the 'symbol' key is present in the 'dataset' and 'dataset' is not empty
        if 'symbol' not in dataset or not dataset:
            logging.info("Symbol not found in the dataset or the dataset is empty.") 
            return None
        
        try:
            nse_api = _nseData.NSE()
            df = nse_api.getHistoricalData(dataset['symbol'], 'EQ', dataset['start_date'], dataset['end_date'])
            if df is not None:
                selected_columns = ['open', 'high', 'low', 'close', 'volume']
                df_subset = df[selected_columns]
                return df_subset
            else:
                logging.info("Error fetching data or data is empty.")
        except Exception as e:
            logging.info(f"Error fetching data for {dataset['symbol']}: {str(e)}")
            return None

    def fetch_backtest_historical_data(self, args):
        stock_historical_data = {}
        filter_stocks = args['stock_list']
        filter_data_interval = args['backtest_timeframe']
        filter_start_date = args['backtest_start_date']
        filter_end_date = args['backtest_end_date']
        
        # Determine the directory based on the filter_data_interval
        match filter_data_interval.lower():
            case '1m':
                directory = HISTORICAL_DATA_PATH_1M
            case '3m':
                directory = HISTORICAL_DATA_PATH_3M
            case '5m':
                directory = HISTORICAL_DATA_PATH_5M
            case '10m':
                directory = HISTORICAL_DATA_PATH_10M
            case '15m':
                directory = HISTORICAL_DATA_PATH_15M
            case '30m':
                directory = HISTORICAL_DATA_PATH_30M
            case '60m':
                directory = HISTORICAL_DATA_PATH_60M
            case '1d':
                directory = HISTORICAL_DATA_PATH_1D        
            case _:
                self.invalid_option(filter_data_interval.lower())
       
        # Use read_csv_files_in_directory for parallel file reading
        stock_historical_data = self.read_csv_files_in_directory(directory, filter_stocks, filter_start_date, filter_end_date)
        return stock_historical_data


    def read_csv_file(self, filepath, filter_stocks, filter_start_date, filter_end_date):
        stock_name = os.path.basename(filepath).split('.')[0]
        if stock_name in filter_stocks:
            logging.info(f'Reading file {filepath}')
            stock_data = pd.read_csv(filepath)
            stock_data['date'] = pd.to_datetime(stock_data['date'])
            stock_data = stock_data[(stock_data['date'] >= filter_start_date) & (stock_data['date'] <= filter_end_date)]
            return stock_name, stock_data

    def read_csv_files_in_directory(self, directory, filter_stocks, filter_start_date, filter_end_date):
        collect_historical_data = {}
        
        # Get the list of files that end with ".csv" and match filter_stocks
        files = [os.path.join(directory, filename) for filename in os.listdir(directory) 
            if filename.endswith(".csv") and os.path.basename(filename).split('.')[0] in filter_stocks]
    
        # Use ProcessPoolExecutor for parallel processing
        with ProcessPoolExecutor() as executor:
            # Use functools.partial to create a partial function with fixed arguments
            partial_read_csv_file = partial(self.read_csv_file, filter_stocks = filter_stocks, filter_start_date = filter_start_date, filter_end_date = filter_end_date)
        
            # Use executor.map to map the partial function to each file in parallel
            results = executor.map(partial_read_csv_file, files)
    
        # Iterate over the results and populate stock_historical_data dictionary
        for stock_name, stock_data in results:
            collect_historical_data[stock_name] = stock_data
    
        return collect_historical_data
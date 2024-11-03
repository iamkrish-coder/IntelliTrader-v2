# Constants
import datetime
import os

now = datetime.datetime.now()
CURRENT_DATE = now.strftime("%Y-%m-%d")
SECRET_NAME = 'IntelliTrader'
REGION_NAME = 'ap-south-1'
HOST = '127.0.0.1'
PORT = '5000'
ARN = 'arn'
AWS = 'aws'
SNS = 'sns'
SQS = 'sqs'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../IntelliTrader'))
ALGORITHM_PATH = os.path.join(BASE_DIR, 'backend', 'algorithms')
CONFIGURATION_PATH = os.path.join(BASE_DIR, 'backend', 'configurations')
OUTPUT_PATH = os.path.join(BASE_DIR, 'backend', 'output')
DATA_PATH = os.path.join(BASE_DIR, 'backend', 'data')
CACHE_PATH = os.path.join(BASE_DIR, 'backend', 'cache')
TEMPLATES_PATH = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_FILE_PATH = os.path.join(BASE_DIR, 'frontend', 'static')
CACHE_CONNECTION_PATH = os.path.join(BASE_DIR, 'backend', 'cache', CURRENT_DATE, 'connection')
ACCESS_TOKEN_PATH = os.path.join(CACHE_CONNECTION_PATH, '.zerodha_access_token')
REQUEST_TOKEN_PATH = os.path.join(CACHE_CONNECTION_PATH, '.zerodha_request_token')
ENCRYPT_TOKEN_PATH = os.path.join(CACHE_CONNECTION_PATH, '.zerodha_encrypt_token')
EQUITY_BASKET = os.path.join(BASE_DIR, 'backend', 'data', 'basket', 'equity_basket.csv')
INDEX_OPTIONS_BASKET = os.path.join(BASE_DIR, 'backend', 'data', 'basket', 'index_options_basket.csv')
STOCK_OPTIONS_BASKET = os.path.join(BASE_DIR, 'backend', 'data', 'basket', 'stock_options_basket.csv')
FUTURES_BASKET = os.path.join(BASE_DIR, 'backend', 'data', 'basket', 'futures_basket.csv')
HISTORICAL_DATA_PATH_1M = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '1minute')
HISTORICAL_DATA_PATH_3M = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '3minute')
HISTORICAL_DATA_PATH_5M = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '5minute')
HISTORICAL_DATA_PATH_10M = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '10minute')
HISTORICAL_DATA_PATH_15M = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '15minute')
HISTORICAL_DATA_PATH_30M = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '30minute')
HISTORICAL_DATA_PATH_60M = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '60minute')
HISTORICAL_DATA_PATH_1D = os.path.join(BASE_DIR, 'backend', 'data', 'historical', '1day')
APP_CONFIGURATION_FILE = 'app_configuration.json'
TABLE_CONFIGURATION_FILE = 'table_configuration.json'
MINUTE_1M = '1minute'
MINUTE_2M = '2minute'
MINUTE_3M = '3minute'
MINUTE_5M = '5minute'
MINUTE_10M = '10minute'
MINUTE_15M = '15minute'
MINUTE_30M = '30minute'
MINUTE_60M = '60minute'
TODAY_1M = 'today1minute'
TODAY_2M = 'today2minute'
TODAY_3M = 'today3minute'
TODAY_5M = 'today5minute'
TODAY_15M = 'today15minute'
TODAY_30M = 'today30minute'
TODAY_60M = 'today60minute'
HOUR_1H = '1hour'
HOUR_2H = '2hour'
HOUR_4H = '4hour'
HOUR = 'hour'
DAY = 'day'
WEEK = 'week'
MONTH = 'month'
MINUTE = 'minute'
DATABASE_LOGGER_NAME = 'database'
STRATEGY_LOGGER_NAME = 'strategy'
SIGNAL_LOGGER_NAME = 'signal'
TRADE_LOGGER_NAME = 'trade'
MONITORING_LOGGER_NAME = 'monitoring'
INTELLITRADER_LOGGER_NAME = 'intelliTrader'
ASYNCIO = 'asyncio'
BLOCKING = 'blocking'
BACKGROUND = 'background'
TABLE_TOPICS = "topics"
TABLE_QUEUES = 'queues'
TABLE_STRATEGIES = 'strategies'
TABLE_TRADES = "trades"
TABLE_SIGNAL = "signal"
TABLE_USERS = "users"
CACHE_STRATEGIES_DIR = "strategies"
CACHE_TOPICS_DIR = "topics"
CACHE_CANDLESTICKS_DIR = "candlesticks"
CACHE_CONNECTION_DIR = "connection"
CACHE_INSTRUMENTS_DIR = "instruments"
IS_PUBLISHED = "is_published"
FIFO = "fifo"
STANDARD = "standard"
SIGNAL_EVENT_GET = 'get'
SIGNAL_EVENT_POST = 'post'
# Products
PRODUCT_MIS = "MIS"
PRODUCT_CNC = "CNC"
PRODUCT_NRML = "NRML"
PRODUCT_CO = "CO"
# Order types
ORDER_TYPE_MARKET = "MARKET"
ORDER_TYPE_LIMIT = "LIMIT"
ORDER_TYPE_SLM = "SL-M"
ORDER_TYPE_SL = "SL"
ORDER_TYPE_GTT = "GTT"
# Varities
VARIETY_REGULAR = "regular"
VARIETY_CO = "co"
VARIETY_AMO = "amo"
VARIETY_ICEBERG = "iceberg"
VARIETY_AUCTION = "auction"
# Transaction type
TRANSACTION_TYPE_BUY = "BUY"
TRANSACTION_TYPE_SELL = "SELL"
# Validity
VALIDITY_DAY = "DAY"
VALIDITY_IOC = "IOC"
VALIDITY_TTL = "TTL"
# Position Type
POSITION_TYPE_DAY = "day"
POSITION_TYPE_OVERNIGHT = "overnight"
# Exchanges
EXCHANGE_NSE = "NSE"
EXCHANGE_BSE = "BSE"
EXCHANGE_NFO = "NFO"
EXCHANGE_CDS = "CDS"
EXCHANGE_BFO = "BFO"
EXCHANGE_MCX = "MCX"
EXCHANGE_BCD = "BCD"
# Margins segments
MARGIN_EQUITY = "equity"
MARGIN_COMMODITY = "commodity"
# Status constants
STATUS_COMPLETE = "COMPLETE"
STATUS_REJECTED = "REJECTED"
STATUS_CANCELLED = "CANCELLED"
# GTT order type
GTT_TYPE_OCO = "two-leg"
GTT_TYPE_SINGLE = "single"
# GTT order status
GTT_STATUS_ACTIVE = "active"
GTT_STATUS_TRIGGERED = "triggered"
GTT_STATUS_DISABLED = "disabled"
GTT_STATUS_EXPIRED = "expired"
GTT_STATUS_CANCELLED = "cancelled"
GTT_STATUS_REJECTED = "rejected"
GTT_STATUS_DELETED = "deleted"
# ORDER RESPONSE
ORDER_VALIDITY_THRESHOLD_MINUTES = 5
ORDER_IS_OPEN = "OPEN"
ORDER_IS_PENDING = "PENDING"
ORDER_IS_ACTIVE = "ACTIVE"
FO_CE = "CE"
FO_PE = "PE"
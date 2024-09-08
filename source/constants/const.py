# Constants
import datetime

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
SOURCE_PATH = './source'
ALGORITHM_PATH = './source/algorithms'
CONFIGURATION_PATH = './source/configurations'
OUTPUT_PATH = './source/output'
DATA_PATH = './source/data'
TEMPLATES_PATH = './source/templates'
CACHE_PATH = './source/cache'
STATIC_FILE_PATH = './source/static'
CACHE_CONNECTION_PATH = f'./source/cache/{CURRENT_DATE}/connection'
ACCESS_TOKEN_PATH = f'./source/cache/{CURRENT_DATE}/connection/.zerodha_access_token'
REQUEST_TOKEN_PATH = f'./source/cache/{CURRENT_DATE}/connection/.zerodha_request_token'
ENCRYPT_TOKEN_PATH = f'./source/cache/{CURRENT_DATE}/connection/.zerodha_encrypt_token'
DEFAULT_BASKET = './source/data/basket/default_basket.csv'
HISTORICAL_DATA_PATH_1M = './source/data/historical/1minute'
HISTORICAL_DATA_PATH_3M = './source/data/historical/3minute'
HISTORICAL_DATA_PATH_5M = './source/data/historical/5minute'
HISTORICAL_DATA_PATH_10M = './source/data/historical/10minute'
HISTORICAL_DATA_PATH_15M = './source/data/historical/15minute'
HISTORICAL_DATA_PATH_30M = './source/data/historical/30minute'
HISTORICAL_DATA_PATH_60M = './source/data/historical/60minute'
HISTORICAL_DATA_PATH_1D = './source/data/historical/1day'
APP_CONFIGURATION_FILE = 'app_config.json'
TABLE_CONFIGURATION_FILE = 'table_config.json'
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
TABLE_ALERTS = "alerts"
CACHE_STRATEGIES_DIR = "strategies"
CACHE_TOPICS_DIR = "topics"
CACHE_CANDLESTICKS_DIR = "candlesticks"
CACHE_CONNECTION_DIR = "connection"
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

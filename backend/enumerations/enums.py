# ENUMS
from enum import Enum
from backend.constants.const import ARN


class Logger(Enum):
    INTELLITRADER_LOGGER = "intellitrader_logger"


class HTTPStatus(Enum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501 
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class AWS_SQS(Enum):
    ARN = 'arn'
    AWS = 'aws'
    SQS = 'sqs'
    REGION = 'ap-south-1'
    ACCOUNT_ID = '265153260161'
    URL = 'https://sqs.ap-south-1.amazonaws.com'


class StrategyDefinition(Enum):
    BUY = "buy"
    SELL = "sell"
    STOP_LOSS = "stop_loss"
    TRAIL_PROFIT = "trail_profit"
    TRAIL_STOP_LOSS = "trail_stop_loss"
    EXIT = "exit"


class AWS_SNS(Enum):
    ARN = 'arn'
    AWS = 'aws'
    SNS = 'sns'
    REGION = 'ap-south-1'
    ACCOUNT_ID = '265153260161'


class Cache_Type(Enum):
    DISK = "disk"
    MEMORY = "memory"


class Tables(Enum):
    TABLE_TOPICS = 'topics'
    TABLE_QUEUES = 'queues'
    TABLE_SIGNALS = 'signals'
    TABLE_TRADES = 'trades'
    TABLE_STRATEGIES = 'strategies'
    TABLE_USERS = 'users'


class Events(Enum):
    PUT = 'put'
    GET = 'get'
    QUERY = 'query'
    SCAN = 'scan'
    UPDATE = 'update'
    DELETE = 'delete'


class Market_Sentiment(Enum):
    POSITIVE = 'POSITIVE'
    NEGATIVE = 'NEGATIVE'


class Option_Type(Enum):
    CE = 1
    PE = 2
    ALL = 3


class Position_Size(Enum):
    CAPITAL_BASED = 1
    RISK_BASED = 2
    MANUAL = 3


class Instrument_Type(Enum):
    EQUITY = 1
    OPTIONS = 2
    FUTURES = 3


class Variety(Enum):
    REGULAR = 1
    AMO = 2
    CO = 3
    ICEBERG = 4
    AUCTION = 5


class Exchange(Enum):
    NSE = 1
    BSE = 2
    NFO = 3


class Transaction_Type(Enum):
    BUY = 1
    SELL = 2
    SL = 3
    TP = 4
    TSL = 5
    EXIT = 6

class Product(Enum):
    CNC = 1
    NRML = 2
    MIS = 3


class Order_Type(Enum):
    MARKET = 1
    LIMIT = 2
    SL = 3
    SL_M = 4
    GTT = 5
    CANCEL = 6
    MODIFY = 7
    LIST = 8


class Validity(Enum):
    DAY = 1
    IOC = 2
    TTL = 3


class Strategy_Type(Enum):
    LONG = 1
    SHORT = 2


class Default_Price_Limit(Enum):
    LTP = 1
    OPEN = 2
    HIGH = 3
    LOW = 4
    CLOSE = 5


class RSI(Enum):
    RSI_5 = 5
    RSI_8 = 8
    RSI_10 = 10
    RSI_14 = 14
    RSI_21 = 21


class WMA(Enum):
    WMA_5 = 5
    WMA_8 = 8
    WMA_10 = 10
    WMA_14 = 14
    WMA_21 = 21
    WMA_34 = 34
    WMA_50 = 50
    WMA_100 = 100
    WMA_200 = 200


class SMA(Enum):
    SMA_5 = 5
    SMA_8 = 8
    SMA_10 = 10
    SMA_14 = 14
    SMA_21 = 21
    SMA_50 = 50
    SMA_100 = 100
    SMA_200 = 200


class EMA(Enum):
    EMA_5 = 5
    EMA_8 = 8
    EMA_10 = 10
    EMA_14 = 14
    EMA_21 = 21
    EMA_50 = 50
    EMA_100 = 100
    EMA_200 = 200


class Williams_R(Enum):
    WILLIAMSR_5 = 5
    WILLIAMSR_8 = 8
    WILLIAMSR_10 = 10
    WILLIAMSR_14 = 14
    WILLIAMSR_21 = 21
    WILLIAMSR_50 = 50
    WILLIAMSR_100 = 100
    WILLIAMSR_200 = 200


class Supertrend(Enum):
    SUPERTREND_4_2 = [4, 2]
    SUPERTREND_7_3 = [7, 3]
    SUPERTREND_10_3 = [10, 3]
    SUPERTREND_14_3 = [14, 3]
    SUPERTREND_20_2 = [20, 2]
    SUPERTREND_50_10 = [50, 10]


class Bollinger_Bands(Enum):
    BOLLINGERBANDS_20_2 = [20, 2]
    BOLLINGERBANDS_14_1 = [14, 1]
    BOLLINGERBANDS_30_3 = [30, 3]
    BOLLINGERBANDS_50_2 = [50, 2]
    BOLLINGERBANDS_100_5 = [100, 5]


class MACD(Enum):
    MACD_12_26_9 = [12, 26, 9]
    MACD_8_17_9 = [8, 17, 9]
    MACD_5_13_9 = [5, 13, 9]
    MACD_10_20_5 = [10, 20, 5]
    MACD_14_28_7 = [14, 28, 7]


class Stochastic(Enum):
    STOCHASTIC_5_3_3 = [5, 3, 3]
    STOCHASTIC_10_3_3 = [10, 3, 3]
    STOCHASTIC_14_3_3 = [14, 3, 3]
    STOCHASTIC_20_5_5 = [20, 5, 5]
    STOCHASTIC_50_14_14 = [50, 14, 14]


class TrueRange(Enum):
    TRUERANGE_5 = 5
    TRUERANGE_8 = 8
    TRUERANGE_10 = 10
    TRUERANGE_14 = 14
    TRUERANGE_21 = 21
    TRUERANGE_50 = 50
    TRUERANGE_100 = 100
    TRUERANGE_200 = 200


class AverageTrueRange(Enum):
    AVERAGETRUERANGE_5 = 5
    AVERAGETRUERANGE_8 = 8
    AVERAGETRUERANGE_10 = 10
    AVERAGETRUERANGE_14 = 14
    AVERAGETRUERANGE_21 = 21
    AVERAGETRUERANGE_50 = 50
    AVERAGETRUERANGE_100 = 100
    AVERAGETRUERANGE_200 = 200


class Modules(Enum):
    AUTHENTICATION = "AU"
    DASHBOARD = "DA"
    ORDERS = "OR"
    POSITIONS = "PO"
    STRATEGIES = "ST"
    REPORTS = "RE"
    SETTINGS = "SE"
    TRADES = "TR"


class Procedures(Enum):
    CREATE_USER_ACCOUNT_SP = "it_au_create_user_account_sp"
    CREATE_SESSION_SP = "it_au_create_session_sp"

class Functions(Enum):
    GET_USER_BY_EMAIL_FN = "it_au_get_user_by_email_fn"
    GET_USER_BY_ACCOUNT_FN = "it_au_get_user_by_account_fn"

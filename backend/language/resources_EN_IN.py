from backend.enumerations.resource_string_enums import INFO, ERROR, WARN

ResourceStrings = {

    #####################################################################################################
    # INFO MESSAGES
    #####################################################################################################

    INFO.CONNECT_KITE_COMPLETE: "Connection to Kite Connect API ...COMPLETE!",
    INFO.NEW_CONNECTION_REQUEST_COMPLETE: "New Connection Request to Kite Connect API ...COMPLETE!",
    INFO.RETRIEVING_SECRET_KEYS_COMPLETE: "Retrieving Secret Keys From AWS Secrets Manager ...COMPLETE!",
    INFO.GENERATE_KITE_REQUEST_TOKEN_COMPLETE: "Generate Kite Request Token ...COMPLETE!",
    INFO.GENERATE_KITE_ACCESS_TOKEN_COMPLETE: "Generate Kite Access Token ...COMPLETE!",
    INFO.FETCHING_OHLCV_DATA: "Fetching OHLCV data for {}, {}, {} ...COMPLETE!",
    INFO.FETCHING_INDICATOR_DATA: "Fetching Indicator data for {}, {}, {} ...COMPLETE!",
    INFO.ANALYZING_LOCAL_MARKET_SENTIMENT_COMPLETE: "Analyzing local market sentiment ...COMPLETE!",
    INFO.ANALYZING_GLOBAL_MARKET_SENTIMENT_COMPLETE: "Analyzing global market sentiment ...COMPLETE!",
    INFO.ALERTS_PUBLISHED_COMPLETE: "Alerts Published ...COMPLETE!",
    INFO.MARKET_ORDER_PLACED: "MARKET ORDER PLACED.",
    INFO.LIMIT_ORDER_PLACED: "LIMIT ORDER PLACED SUCCESSFULLY.",
    INFO.SINGLE_LEG_GTT_PLACED: "SINGLE LEG GTT ORDER PLACED.",
    INFO.GTT_OCO_PLACED: "GTT OCO ORDER PLACED.",
    INFO.EVALUATING_STRATEGY: "EVALUATING STRATEGY: {}",
    INFO.MESSAGE_PUBLISHED: "MESSAGE PUBLISHED: {}",
    INFO.REDIS_SERVER_STARTED: "REDIS SERVER STARTED.",
    INFO.REDIS_SERVER_ALREADY_RUNNING: "REDIS SERVER ALREADY RUNNING.",
    INFO.REDIS_SERVER_STOPPED: "REDIS SERVER STOPPED SUCCESSFULLY.",
    INFO.SUCCESSFULLY_CONNECTED: "Successfully connected.",
    INFO.CURRENT_MODE: "Current mode: {}",

    #####################################################################################################
    # WARNING MESSAGES
    #####################################################################################################

    WARN.NO_DATA_FOUND: "No data found for {}",

    #####################################################################################################
    # ERROR MESSAGES
    #####################################################################################################

    ERROR.SYMBOL_NOT_FOUND: "Symbol not found in the dataset or the dataset is empty.",
    ERROR.ERROR_FETCHING_DATA: "Error fetching data or data is empty.",
    ERROR.ERROR_RETRIEVING_APPLICATION_SETTINGS: "An error occurred retrieving Application Settings: {}",
    ERROR.ORDER_PLACEMENT_FAILED: "Order placement failed: {}",
    ERROR.ERROR_PLACING_GTT_OCO_ORDER: "Error placing gtt oco order: {}",
    ERROR.AN_ERROR_OCCURRED: "An error occurred: {}",
    ERROR.CONNECTION_CLOSED: "Connection closed: {} - {}",
    ERROR.CONNECTION_ERROR: "Connection error: {} - {}",
    ERROR.RECONNECT_FAILED: "Reconnect failed."
}

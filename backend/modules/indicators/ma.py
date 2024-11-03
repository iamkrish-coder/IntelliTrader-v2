import numpy as np


def sma(dataset, period=5):
    """
    Calculate the Simple Moving Average (SMA) based on the provided dataset.

    Parameters:
    - dataset (pd.DataFrame): A pandas DataFrame containing OHLCV (Open, High, Low, Close, Volume) values.
    - period (int): The number of periods to consider for SMA calculation. Default is 5.

    Returns:
    - list: A list of SMA values (float) calculated based on the dataset.
    """

    # Check if dataset contains the required columns
    data = dataset['close'] if 'close' in dataset else None
    if data is not None:
        # Check if the data has sufficient length for SMA calculations
        if len(data) >= period:
            sma_values = data.rolling(window=period).mean()
            sma_values = sma_values.dropna().tolist()
            sma = [round(value, 2) for value in sma_values]
            return sma
    return None


def ema(dataset, period=5):
    """
    Calculate the Exponential Moving Average (EMA) based on the provided dataset.

    Parameters:
    - dataset (pd.DataFrame): A pandas DataFrame containing OHLCV (Open, High, Low, Close, Volume) values.
    - period (int): The number of periods to consider for EMA calculation. Default is 5.

    Returns:
    - list: A list of EMA values (float) calculated based on the dataset.
    """

    # Check if dataset contains the required columns
    data = dataset['close'] if 'close' in dataset else None
    if data is not None:
        # Check if the data has sufficient length for EMA calculations
        if len(data) >= period:
            ema_values = data.ewm(span=period, adjust=False).mean()
            ema_values = ema_values.dropna().tolist()
            ema = [round(value, 2) for value in ema_values]
            return ema
    return None


def wma(dataset, period=5):
    """
    Calculate the Weighted Moving Average (WMA) based on the provided dataset.

    Parameters:
    - dataset (pd.DataFrame): A pandas DataFrame containing OHLCV (Open, High, Low, Close, Volume) values.
    - period (int): The number of periods to consider for WMA calculation. Default is 5.

    Returns:
    - list: A list of WMA values (float) calculated based on the dataset.
    """

    # Check if dataset contains the required columns
    data = dataset['close'] if 'close' in dataset else None
    if data is not None:
        # Check if the data has sufficient length for WMA calculations
        if len(data) >= period:
            weights = np.arange(1, period + 1)
            wma_values = data.rolling(window=period).apply(lambda prices: np.dot(prices, weights) / weights.sum(),
                                                           raw=True)
            wma_values = wma_values.dropna().tolist()
            wma = [round(value, 2) for value in wma_values]
            return wma
    return None

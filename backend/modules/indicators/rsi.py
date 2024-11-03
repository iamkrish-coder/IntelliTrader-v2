import numpy as np


def rsi(dataset, period=14):
    """
    Calculate the Relative Strength Index (RSI) based on the provided dataset.

    Parameters:
    - dataset (pd.DataFrame): A pandas DataFrame containing OHLCV (Open, High, Low, Close, Volume) values.
    - period (int): The number of periods to consider for RSI calculation. Default is 14.

    Returns:
    - list: A list of closing prices (float) calculated based on the dataset.
    """

    # Check if dataset contains the required columns
    data = dataset['close'] if 'close' in dataset else None

    if data is None:
        return None

    # Check if data has sufficient length for RSI calculations
    if len(data) < period:
        return None

    close_prices = [float(x) for x in data]
    deltas = np.diff(close_prices)
    seed = deltas[:period + 1]
    up_periods = []
    down_periods = []

    up_periods.append(sum(x for x in seed if x >= 0) / period)
    down_periods.append(abs(sum(x for x in seed if x < 0) / period))

    for i in range(period + 1, len(close_prices)):
        delta = deltas[i - 1]
        if delta > 0:
            up_periods.append((up_periods[-1] * (period - 1) + delta) / period)
            down_periods.append((down_periods[-1] * (period - 1)) / period)
        else:
            up_periods.append((up_periods[-1] * (period - 1)) / period)
            down_periods.append((down_periods[-1] * (period - 1) - delta) / period)

    try:
        down_periods = [0.001 if x == 0.0 else x for x in down_periods]
        rs = np.array(up_periods) / np.array(down_periods)
        rsi = np.round(100 - (100 / (1 + rs)), 2).tolist()
    except RuntimeWarning:
        rsi = None

    return rsi

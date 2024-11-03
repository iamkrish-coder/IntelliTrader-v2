import numpy as np


def macd(dataset, period=[12, 26, 9]):
    short_period = period[0]
    long_period = period[1]
    signal_period = period[2]

    # Check if dataset contains the required columns
    data = dataset['close'] if 'close' in dataset else None

    if data is not None and not data.empty:
        # Check if data has sufficient length for MACD calculations
        if len(data) < long_period:
            return None, None, None

        # Calculate the short-term exponential moving average (EMA)
        ema_short = data.ewm(span=short_period, adjust=True).mean()

        # Calculate the long-term exponential moving average (EMA)
        ema_long = data.ewm(span=long_period, adjust=True).mean()

        # Calculate the MACD line
        macd_line = ema_short - ema_long

        # Calculate the signal line (exponential moving average of MACD line)
        signal_line = macd_line.ewm(span=signal_period, adjust=True).mean()

        # Calculate the MACD histogram
        macd_histogram = macd_line - signal_line

        # Round the values to 2 decimal places
        macd_line = np.round(macd_line, 2).tolist()
        signal_line = np.round(signal_line, 2).tolist()
        macd_histogram = np.round(macd_histogram, 2).tolist()

        return macd_line, signal_line, macd_histogram
    else:
        return None, None, None

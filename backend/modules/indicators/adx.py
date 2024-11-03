import pandas as pd
import numpy as np


def adx(dataset, period=14):
    # Check if dataset contains the required columns
    data = dataset if 'close' in dataset and 'high' in dataset and 'low' in dataset else None

    if data is not None and not data.empty:
        # Check if the data has sufficient length for Williams %R calculations
        if len(data) < period:
            return None

    # Calculate the True Range (TR)
    data['tr'] = np.max([data['high'] - data['low'],
                         abs(data['high'] - data['close'].shift()),
                         abs(data['low'] - data['close'].shift())], axis=0)

    # Calculate the Directional Movement (DM)
    data['up_move'] = data['high'].diff()
    data['down_move'] = data['low'].diff()
    data['up_move'] = np.where(data['up_move'] > 0, data['up_move'], 0)
    data['down_move'] = np.where(data['down_move'] < 0, -data['down_move'], 0)

    # Calculate the True Range (TR), Positive Directional Index (+DI), and Negative Directional Index (-DI) for the first period
    tr_period = data['tr'][:period].sum()
    up_move_period = data['up_move'][:period].sum()
    down_move_period = data['down_move'][:period].sum()

    # Initialize lists to store the Positive Directional Index (+DI), Negative Directional Index (-DI), and True Range (TR) values
    di_plus_values = []
    di_minus_values = []
    tr_values = []

    # Calculate the True Range (TR), Positive Directional Index (+DI), Negative Directional Index (-DI), and Average True Range (ATR) for the remaining periods
    for i in range(period, len(data)):
        tr = tr_period - (tr_period / period) + data['tr'].iloc[i]
        up_move = up_move_period - (up_move_period / period) + data['up_move'].iloc[i]
        down_move = down_move_period - (down_move_period / period) + data['down_move'].iloc[i]

        tr_values.append(tr)
        di_plus = 100 * (up_move / tr)
        di_minus = 100 * (down_move / tr)
        di_plus_values.append(di_plus)
        di_minus_values.append(di_minus)

        tr_period = tr
        up_move_period = up_move
        down_move_period = down_move

    # Calculate the Average Directional Index (ADX)
    dx_values = 100 * (abs(np.array(di_plus_values) - np.array(di_minus_values)) / (
                np.array(di_plus_values) + np.array(di_minus_values)))
    adx_values = pd.Series(dx_values).rolling(window=period).mean()

    return adx_values

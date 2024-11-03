import pandas as pd
from stocktrends import Renko


def renko(dataset, size=2):
    # Check if dataset contains the required columns
    data = dataset if 'open' in dataset and 'high' in dataset and 'low' in dataset and 'close' in dataset else None
    data.reset_index(inplace=True)
    r = Renko(data)
    r.brick_size = size
    renko_bricks = r.get_ohlc_data()

    return renko_bricks

def stochastic(dataset, period=14, smoothing=3):
    # Check if dataset contains the required columns
    data = dataset if 'close' in dataset and 'high' in dataset and 'low' in dataset else None
    if data is not None and not data.empty:
        # Check if the data has sufficient length for ATR calculations
        if len(data) < period:
            return None

        # Calculate the lowest low and highest high over the given period
        data['lowest_low'] = data['low'].rolling(window=period).min()
        data['highest_high'] = data['high'].rolling(window=period).max()

        # Calculate %K and %D
        data['%K'] = 100 * (data['close'] - data['lowest_low']) / (data['highest_high'] - data['lowest_low'])
        data['%D'] = data['%K'].rolling(window=smoothing).mean()

        return data['%K'], data['%D']

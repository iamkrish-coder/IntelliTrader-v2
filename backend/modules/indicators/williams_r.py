def williams_r(dataset, period=14, factor=100):
    # Check if dataset contains the required columns
    data = dataset if 'close' in dataset else None

    if data is not None and not data.empty:
        # Check if the data has sufficient length for Williams %R calculations
        if len(data) < period:
            return None

        highest_highs = []
        lowest_lows = []
        williams_r_line = []

        for i in range(period - 1, len(data)):
            highest_high = max(data['high'].iloc[i - period + 1:i + 1])
            lowest_low = min(data['low'].iloc[i - period + 1:i + 1])
            highest_highs.append(highest_high)
            lowest_lows.append(lowest_low)
            wr = (highest_high - data['close'].iloc[i]) / (highest_high - lowest_low) * -100
            williams_r_line.append(wr)

        return williams_r_line

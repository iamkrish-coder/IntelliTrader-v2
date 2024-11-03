def bollinger_bands(dataset, period=20, num_std=2):
    # Check if dataset contains the required columns
    data = dataset if 'close' in dataset else None

    if data is not None and not data.empty:
        # Check if the data has sufficient length for Williams %R calculations
        if len(data) < period:
            return None

    # Calculate the rolling mean and standard deviation
    rolling_mean = data['Close'].rolling(period=period).mean()
    rolling_std = data['Close'].rolling(period=period).std()

    # Calculate the upper and lower bands
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    return rolling_mean, upper_band, lower_band

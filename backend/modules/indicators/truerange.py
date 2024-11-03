def truerange(dataset, period=14):
    """
    Calculate the True Range based on the provided dataset.

    Parameters:
    - dataset (pd.DataFrame): A pandas DataFrame containing OHLCV (Open, High, Low, Close, Volume) values.
    - period (int): The number of periods to consider for True Range calculation. Default is 14.

    Returns:
    - list: A list of True Range values (float) calculated based on the dataset.
    """

    # Check if dataset contains the required columns
    data = dataset if 'close' in dataset and 'high' in dataset and 'low' in dataset else None
    if data is not None and not data.empty:
        # Extract the necessary columns from the data
        close_prices = data['close'].astype(float)
        high_prices = data['high'].astype(float)
        low_prices = data['low'].astype(float)

        # Check if the data has sufficient length for True Range calculations
        if len(data) < period:
            return None

        truerange_values = []
        for i in range(len(data)):
            if i == 0:
                # True Range for the first period is the high - low
                tr = high_prices[i] - low_prices[i]
            else:
                # Calculate the three potential ranges
                range1 = high_prices[i] - low_prices[i]
                range2 = abs(high_prices[i] - close_prices[i - 1])
                range3 = abs(low_prices[i] - close_prices[i - 1])
                # True Range is the maximum of the three ranges
                tr = max(range1, range2, range3)

            truerange_values.append(tr)

        truerange = [round(float(value), 2) for value in truerange_values]

        return truerange

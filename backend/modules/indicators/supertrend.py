def supertrend(dataset, period=[7, 3]):
    # Check if dataset contains the required columns
    if 'close' not in dataset or 'high' not in dataset or 'low' not in dataset:
        return None

    dataset['close'] = dataset['close'].astype(float)
    dataset['high'] = dataset['high'].astype(float)
    dataset['low'] = dataset['low'].astype(float)

    # Calculate Average True Range (ATR)
    dataset['tr0'] = abs(dataset['high'] - dataset['low'])
    dataset['tr1'] = abs(dataset['high'] - dataset['close'].shift())
    dataset['tr2'] = abs(dataset['low'] - dataset['close'].shift())
    dataset['true_range'] = dataset[['tr0', 'tr1', 'tr2']].max(axis=1)
    dataset['atr'] = dataset['true_range'].rolling(period[0]).mean()

    # Calculate Supertrend
    dataset['upper_band'] = (dataset['high'] + dataset['low']) / 2 + period[1] * dataset['atr']
    dataset['lower_band'] = (dataset['high'] + dataset['low']) / 2 - period[1] * dataset['atr']
    dataset['supertrend'] = None

    for i in range(period[0], len(dataset)):
        if dataset['close'].iloc[i - 1] <= dataset['upper_band'].iloc[i - 1]:
            dataset.loc[dataset.index[i], 'supertrend'] = dataset.loc[dataset.index[i], 'upper_band']
        elif dataset['close'].iloc[i - 1] > dataset['upper_band'].iloc[i - 1]:
            dataset.loc[dataset.index[i], 'supertrend'] = dataset.loc[dataset.index[i], 'lower_band']

    supertrend_values = dataset['supertrend'].dropna().tolist()
    supertrend = [round(float(value), 2) for value in supertrend_values]

    return supertrend

def vwap(dataset, period=None):
    # Check if dataset contains the required columns
    data = dataset if 'volume' in dataset and 'close' in dataset else None

    if data is not None and not data.empty:
        # Check if the data has sufficient length for Williams %R calculations
        if len(data) < 1:
            return None

    # Calculate the cumulative sum of volume multiplied by price
    cum_volume_price = (dataset['volume'] * dataset['close']).cumsum()
    cum_volume = dataset['volume'].cumsum()

    # Calculate the VWAP
    vwap_values = cum_volume_price / cum_volume

    return vwap_values

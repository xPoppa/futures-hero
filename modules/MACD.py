MACD_threshold = 50

def apply_MACD(dataset):
    dataset['12_EMA'] = dataset['close'].ewm(span=12).mean()
    dataset['26_EMA'] = dataset['close'].ewm(span=26).mean()
    dataset['MACD'] = dataset['12_EMA'] - dataset['26_EMA']
    dataset['Signal'] = dataset['MACD'].ewm(span=9).mean()
    dataset['Histogram'] = dataset['MACD'] - dataset['Signal']
    dataset['MACD_long'] = dataset.apply(long_condition, axis=1)
    dataset['MACD_short'] = dataset.apply(short_condition, axis=1)

    clean = dataset[["timestamp", "MACD_long", "MACD_short"]].copy()
    return clean

def long_condition(dataset):
    if  dataset['Signal'] < MACD_threshold and \
        dataset['Histogram'] > 0 : return True 
    else: return False

def short_condition(dataset):
    if  dataset['Signal'] > -MACD_threshold and \
        dataset['Histogram'] < 0 : return True
    else: return False

def test_module():
    import candlestick, heikin_ashi
    klines = candlestick.get_klines("BTCUSDT", "1h")
    # heikin = heikin_ashi.heikin_ashi(klines)
    applyMACD = apply_MACD(klines)
    print("\nMACD.apply_default(klines)")
    print(applyMACD)

# test_module()
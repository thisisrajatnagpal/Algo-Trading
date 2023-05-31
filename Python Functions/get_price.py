def get_price(ref):
    # ref = ohlc['close'].iloc[-1]
    limit_price = ref*(1+0.02/100)
    sl_price = 0.93*limit_price
    return round(limit_price, 1), round(sl_price, 1)

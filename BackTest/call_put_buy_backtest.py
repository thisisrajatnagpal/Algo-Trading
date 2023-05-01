def call_put(ins = "banknifty", last_closing_price, timestamp, CE = True, sl_per = 10, target_per = 20):
    # refer to "options_historical_api.py"
    time = timestamp.time().strftime("%H:%M:%S")
    options_data = ma.get_data(ins, timestamp.date())
    
    if(CE == True):
        print("It is a call! on ", timestamp.date())
        print("The Time is: ", timestamp.time())

        # This function is written in the "Python Functions" folder
        strike_price = get_strike_price(last_closing_price)

        # This function is written "options_historical_api.py" in the "Python Functions" folder
        symbol = get_options_symbol(options_data, strike_price, "CE")
      else:
        print("It is a put! on ", timestamp.date())
        print("The Time is: ", timestamp.time())
        
        # This function is written in the "Python Functions" folder
        strike_price = get_strike_price(last_closing_price, False)
        
        # This function is written "options_historical_api.py" in the "Python Functions" folder
        symbol = get_options_symbol(options_data, strike_price, "PE")

    
    buy_price = options_data[(options_data['symbol'] == symbol) & (options_data['time'] == time)]['open']
    buy_price = float(buy_price)
    sl = (1-sl_per/100)*buy_price
    target = (1+target_per/100)*buy_price
    print(symbol, buy_price, target, sl, time)
    # The list returned from this function will be used to predict the results of this trade
    return [symbol, buy_price, target, sl, time, options_data[options_data['symbol'] == symbol].reset_index()]

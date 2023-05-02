def algo(day, symbol = "NIFTY BANK"):
    if(check_weekend(day) == 1): return 0
    if(data.shape[0] == 0): 
      instrument = instrumentLookup(instrument_df, symbol)
      data = pd.DataFrame(kite.historical_data(instrument, day.date(), day.date(), "15minute"))
      print("It is a public Holiday, no trading today!")
      print("The date is : ", day.date())
      return 0
    
    Condition 1 : 
      # Buy call
      # Checkout call_put function in the Backtest Folder
      # Checkout results function in the "future of trade.py" file
      args = call_put("banknifty", data.iloc[i]['close'],data.iloc[i]['date'])
      results = result(args[0], args[1], args[2], args[3], args[4], args[5])
      return results
    Conditon 2 :
      # Buy put
      # Checkout call_put function in the Backtest Folder
      # Checkout results function in the "future of trade.py" file
      args = call_put("banknifty", data.iloc[i]['close'],data.iloc[i]['date'], False)
      results = result(args[0], args[1], args[2], args[3], args[4], args[5])
      return results
    else: print("No Setup!")
    return 0

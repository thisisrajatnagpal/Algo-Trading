def result(symbol, buy_price, target, SL, time, data):
  # symbol is options symbol with Strike Price and CE/PE
  # buy Price is the price at which the trade by order was executed
  # target is the desired target for the trade, usually 20 percent
  # SL is the stop loss for the trade, usually 10 percent
  
  # getting index of the options data at the time of execution of the trade
  i = data.index[data['time'] == time].tolist()[0]
  
  # initializing some variables used in the later part of the code
  squareoff_time = data.iloc[i]['time']
  squareoff_iter = i
  
  # Since it is 1 minute data, "-30" represents that we do not want to hold the trade if the time is 3 p.m.
  for iter in range (i, data.shape[0] - 30):
    
    # Since, this is the backtesting so we do not have continous data, we assume the target or stop loss hit if the closing price of a candle is in accordance
    closing_price = float(data.iloc[iter]['close'])
     if(closing_price <= SL):
            print("Stop Loss Order Triggered")
            loss = round(buy_price - SL)
            loss_per = (loss/buy_price)*100
            print("You made a loss of INR", loss)
            print("Loss percentage is: ", loss_per)
            print("Your Buy Price was INR", buy_price)
            print("Your sell price was INR", SL)
            print("Order Triggered at timestamp: ", data.iloc[iter]['time'])
            return [ symbol, True, False, loss, buy_price, SL, time, data.iloc[iter]['time']]
      elif(closing_price >= target):
          print("Target Achieved")
          profit = round(target - buy_price)
          profit_per = (profit/buy_price)*100
          print("You made a profit of INR", profit)
          print("profit percentage is: ", profit_per)
          print("Your Buy Price was INR", buy_price)
          print("Your sell price was INR", target)
          print("Order Triggered at timestamp: ", data.iloc[iter]['time'])
          return [symbol,  False, True, profit, buy_price, target, time, data.iloc[iter]['time']]
       # If we are here means nothing happened, neither target was hit nor stop loss, it is time to square off our position
      squareoff_time = data.iloc[iter]['time']
      squareoff_iter = iter
 return [symbol, (float(data.iloc[squareoff_iter]['close'])<=buy_price),
            (float(data.iloc[squareoff_iter]['close'])>buy_price), 
            abs((float(data.iloc[squareoff_iter]['close'])-buy_price)), buy_price,
            float(data.iloc[squareoff_iter]['close']), time, squareoff_time] 


# Please note that the results are supposed to be stored in the following dataframe
# results = pd.DataFrame(columns=['date', 'symbol', 'loss', 'profit', 'profit/loss', 'buy price', 'sell price', 'buy time', 'sell time', 'quantity', 'total'])


# The below is the code to store the results according to a general algorithm, the output of the algorithm should be in the above format by using the given functions
dates = gen_dates("d-m-Y", Number of days from the given date)

# the function to generate the corresponding dates to get the backtesting time duration
def gen_dates(first_date, days):
    duration = dt.timedelta(days)
    from_date = dt.datetime.strptime(first_date, '%d-%m-%Y')
    #print(from_date.strftime("%A"))
    store = []
    for d in range(duration.days + 1):
        day = from_date + dt.timedelta(days=d)
        store.append(day)
    return store
  

for date in dates:
    print("**********************")
    # This is our algorithm
    r = Algorithm(date)
    if(r != 0):
        r = [date.strftime('%m-%d-%Y')] + r
        r.append(int(25))
        r.append(r[4]*r[-1])
        if(r[2] == True):
            r[-1] = -r[-1]
        results.loc[len(results)] = r



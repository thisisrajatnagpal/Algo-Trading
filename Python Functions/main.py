def main(capital):
    a,b = 0,0
    while a < 10:
    # running the loop multiple times to increase the probability of getting the required information in case if connection is not eastablished in one go
        try:
            # getting the open positions of the day
            pos_df = pd.DataFrame(kite.positions()["day"])
            break
        except:
            print("can't extract position data..retrying")
            a+=1
    while b < 10:
      # running the loop multiple times to increase the probability of getting the required information in case if connection is not eastablished in one go
        try:
            # getting the list of orders placed on the current day
            ord_df = pd.DataFrame(kite.orders())
            break
        except:
            print("can't extract order data..retrying")
            b+=1
     for ticker in tickers:
        print("starting passthrough for.....",ticker)    
        try:

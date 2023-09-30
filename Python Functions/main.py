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
            # last traded price of the NSE ticker stock
            ltp = kite.ltp("NSE:" + ticker)["NSE:" + ticker]['last_price']

            # currently quantity is set to one lot per options ticker, it can be changed in util_get_options_symbol function
            ce_symbol, pe_symbol, quantity = util_get_options_symbol(ticker, ltp)
            order_present = False
            
            if(pos_df.shape[0] != 0):
                # if there is an open position
                if(pos_df[pos_df['tradingsymbol'].str.contains(ticker)].shape[0] != 0):    
                    order_present = True
                

            if (not(order_present)):
            # Give some condition here
                Place_SL_Order(ce_symbol, quantity, order_type)
            if(order_present):
                order_id = ord_df.loc[(ord_df['tradingsymbol'].str.contains(ticker)) & (ord_df['status'].isin(["TRIGGER PENDING","OPEN"]))]
                Modify_SL_Order(order_id, order_type)    
        except:
            print("API error for ticker :", ticker)

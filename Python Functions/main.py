def main(capital):
    a,b = 0,0
    while a < 10:
    # running the loop multiple times to increase the probability of getting the required information in case if connection is not established in one go
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
     Open_SL_Orders = ord_df.loc[((ord_df['order_type'] == "SL") & (ord_df['status'] == "OPEN"))]
     if(Open_SL_Orders.shape[0] != 0):
         Close_SL_Order(Open_SL_Orders)
     for ticker in tickers:
        print("starting passthrough for.....",ticker)    
        try:
            # last traded price of the NSE ticker stock
            ltp = kite.ltp("NSE:" + ticker)["NSE:" + ticker]['last_price']

            # currently quantity is set to one lot per options ticker, it can be changed in util_get_options_symbol function
            ce_symbol, pe_symbol, quantity = util_get_options_symbol(ticker, ltp)
            open_position = False
            
            if(pos_df.shape[0] != 0):
                # if there is an open position
                if(pos_df[pos_df['tradingsymbol'].str.contains(ticker)].shape[0] != 0):    
                    open_position = True
                

            if (not(open_position)):
            # Give some condition here
                Place_Order_with_SL(ce_symbol, quantity, order_type)
            if(open_position):
                order_df = ord_df.loc[(ord_df['tradingsymbol'].str.contains(ticker)) & (ord_df['status'].isin(["TRIGGER PENDING","OPEN"]))]
                Modify_SL_Order(order_df, order_type)    
        except:
            print("API error for ticker :", ticker)

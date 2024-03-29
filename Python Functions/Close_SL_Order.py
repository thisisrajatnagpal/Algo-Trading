def Close_SL_Order(order_df):
  for iter in range(order_df.shape[0]):
        if(order_df['order_type'].iloc[iter]!= "SL"):
            print("The order for " + str( order_df['tradingsymbol'].iloc[iter]) + " is not a Stop Loss order")
            continue
        # We have to get the options ticker in order to proceed with the function
        symbol = order_df['tradingsymbol'].iloc[iter]
        # getting last traded price of the ticker from the API, please note that in order to get the last traded price of an options symbol, we have to add the prefix "NFO:"
        ltp = kite.ltp("NFO:" + symbol)["NFO:" + symbol]['last_price']
        if(order_df["transaction_type"].iloc[iter] == "SELL"):
            new_sl_price = (1-0.01)*ltp
        elif(order_df["transaction_type"].iloc[iter] == "BUY"):
            new_sl_price = (1+0.01)*ltp
        i = 0
        while(order_df['status'].iloc[0] == "OPEN" and i<5):   
            kite.modify_order(order_id = order_df["order_id"].iloc[iter],
                        # Setting the old prices of the order to new prices
                        price = new_sl_price,                
                        order_type = kite.ORDER_TYPE_LIMIT,
                        variety = kite.VARIETY_REGULAR) 
            if(order_df["transaction_type"].iloc[iter] == "SELL"):
                new_sl_price = (1-0.01)*new_sl_price
            elif(order_df["transaction_type"].iloc[iter] == "BUY"):
                new_sl_price = (1+0.01)*new_sl_price
            i = i+1
        if not(i<5):
            bot.sendMessage(receiver_id, "Stop Loss order for the " + str(symbol) + " is OPEN and there is not sufficient volume to close it, please close it manually!")

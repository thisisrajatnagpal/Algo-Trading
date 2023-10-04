def Modify_SL_Order(order_df, order_type = "buy"):  
    # We have to get the options ticker in order to proceed with the function
    symbol = order_df['tradingsymbol'].iloc[0]
    # getting last traded price of the ticker from the API, please note that in order to get the last traded price of an options symbol, we have to add the prefix "NFO:"
    ltp = kite.ltp("NFO:" + symbol)["NFO:" + symbol]['last_price']

    # getting the stop loss based on the current traded price of the options ticker
    # leaving first variable out because we just need the stop loss price
    _, new_sl_price = util_get_price(ltp, order_type)
    if(order_type == "buy"):
        # If the order was a buy order, it means the trigger price for the stop loss order is going to be greater than the stop loss price
        tp = round((1+0.01)*new_sl_price, 1)
        if(order_df['price'].iloc[0] < new_sl_price):
        # If the new stop loss price is greater than the previous stop loss price, it means the asset price has moved up and we should move up our stop loss price
            kite.modify_order(order_id = order_df["order_id"].iloc[0],
                        # Setting the old prices of the order to new prices
                        price = new_sl_price,
                        trigger_price = tp,
                        
                        order_type = kite.ORDER_TYPE_SL,
                        variety = kite.VARIETY_REGULAR) 
    elif(order_type == "sell"):
        # If the order was a sell order, it means the trigger price for the stop loss order is going to be less than the stop loss price
        tp = round((1-0.01)*new_sl_price, 1)
        if(order_df['price'].iloc[0] > new_sl_price):
        # If the new stop loss price is less than the previous stop loss price, it means the asset price has gone down and we should move down our stop loss price
            kite.modify_order(order_id = order_df["order_id"].iloc[0],
                        # Setting the old prices of the order to new prices
                        price = new_sl_price,
                        trigger_price = tp,

                        order_type = kite.ORDER_TYPE_SL,
                        variety = kite.VARIETY_REGULAR) 

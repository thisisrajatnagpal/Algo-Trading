def Place_Order_with_trailing_SL_and_target(symbol, quantity, order_type = "buy", sl_per = 7, rr = None):
    if(order_type == "buy"):
    # If we are buing an option then the stop loss order will be selling the option
        t_type = kite.TRANSACTION_TYPE_BUY
        t_type_sl = kite.TRANSACTION_TYPE_SELL
        t_type_target = kite.TRANSACTION_TYPE_SELL
    elif(order_type == "sell"):
    # If we are selling an option then stop loss order will be buying the option
        t_type = kite.TRANSACTION_TYPE_SELL
        t_type_sl = kite.TRANSACTION_TYPE_BUY
        t_type_target = kite.TRANSACTION_TYPE_BUY
    
    # getting last traded price of the ticker from the API, please note that in order to get the last traded price of an options symbol, we have to add the prefix "NFO:"
    ltp = kite.ltp("NFO:" + symbol)["NFO:" + symbol]['last_price']

    # limit price and stop loss price will be adjusted according to the order type, the methodology is written in the utility function 
    limit_price, sl_price = util_get_price(ltp, order_type, sl_per)

    # placing our limit order    
    limit_order = kite.place_order(tradingsymbol=symbol,
                    exchange=kite.EXCHANGE_NFO,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    price=(limit_price),
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR)
    print(limit_order)
    a = 0
    
    while a < 10:
    # This loop is given to avoid some loose connections when we might not get the order list due to connection failure
        try:
            # get the order list
            order_list = kite.orders()
            break
        except:
            print("can't get orders..retrying")
            a+=1
    for order in order_list:
        if order["order_id"]==limit_order:
        # Check for our order
            if order["status"]=="COMPLETE":
            # Check if our order is complete
                # if the order type is buy then the trigger price for the stop loss order is slightly higher than the stop loss price
                if(order_type == "buy"): 
                    tp = round((1+0.01)*sl_price, 1)
                    
                # if the order type is sell then the trigger price for the stop loss order is slightly lower than the stop loss price
                elif(order_type == "sell"): 
                    tp = round((1-0.01)*sl_price, 1)

                # placing the stop loss order
                kite.place_order(tradingsymbol=symbol,
                                exchange = kite.EXCHANGE_NFO,
                                transaction_type = t_type_sl,
                                quantity = quantity,
                                order_type=kite.ORDER_TYPE_SL,
                                price=sl_price,
                                trigger_price = tp,
                                product=kite.PRODUCT_MIS,
                                variety=kite.VARIETY_REGULAR)
            else:
                kite.cancel_order(order_id=limit_order,variety=kite.VARIETY_REGULAR)
     

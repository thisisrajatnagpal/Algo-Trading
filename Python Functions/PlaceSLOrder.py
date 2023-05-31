def placeSLOrder(symbol, quantity):

    t_type = kite.TRANSACTION_TYPE_BUY
    t_type_sl = kite.TRANSACTION_TYPE_SELL
    
    #ohlc_options = fetchOHLC(symbol, "minute", 1, NFO_instrument_df)
    ltp = kite.ltp("NFO:" + symbol)["NFO:" + symbol]['last_price']
    limit_price, sl_price = get_price(ltp)
  
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
        try:
            order_list = kite.orders()
            break
        except:
            print("can't get orders..retrying")
            a+=1
    for order in order_list:
        if order["order_id"]==limit_order:
            if order["status"]=="COMPLETE":
                kite.place_order(tradingsymbol=symbol,
                                exchange=kite.EXCHANGE_NFO,
                                transaction_type=t_type_sl,
                                quantity=quantity,
                                order_type=kite.ORDER_TYPE_SL,
                                price=sl_price,
                                trigger_price = round((1+0.05/100)*sl_price, 1),
                                product=kite.PRODUCT_MIS,
                                variety=kite.VARIETY_REGULAR)
            else:
                kite.cancel_order(order_id=limit_order,variety=kite.VARIETY_REGULAR)

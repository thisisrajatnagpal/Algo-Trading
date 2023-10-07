def util_get_price(ref, order_type = "buy", sl_per = 7, rr=None):
    if(order_type == "buy"):
    # The order is a buy order, stop loss price is 7 percent less than the limit price
        # We have to set the limit price a little higher than the market price to get the order executed
        limit_price = ref*(1+0.005)
        sl_price = (1-sl_per/100)*limit_price
        if(rr!=None): 
            target_price = (1+rr*sl_per/100)*limit_price
            return round(limit_price, 1), round(sl_price, 1), round(target_price, 1)
        else: target_price = None
            return round(limit_price, 1), round(sl_price, 1), target_price
        
    elif(order_type == "sell"):
    # The order is a sell order, stop loss price is 7 percent higher than the limit price
        # We have to set the limit price a little lower to get the order executed
        limit_price = ref*(1-0.005)
        sl_price = (1+sl_per/100)*limit_price
        if(rr!=None): 
            target_price = (1-rr*sl_per/100)*limit_price
            return round(limit_price, 1), round(sl_price, 1), round(target_price, 1)
        else: target_price = None
            return round(limit_price, 1), round(sl_price, 1), target_price

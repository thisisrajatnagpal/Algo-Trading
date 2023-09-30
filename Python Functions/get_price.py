def get_price(ref, order_type = "buy"):
    if(order_type == "buy"):
        limit_price = ref*(1+0.005)
        sl_price = 0.93*limit_price
        return round(limit_price, 1), round(sl_price, 1)
    elif(order_type == "sell"):
        limit_price = ref*(1-0.005)
        sl_price = 1.07*limit_price
        return round(limit_price, 1), round(sl_price, 1)

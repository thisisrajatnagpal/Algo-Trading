def util_util_get_strike_price(ltp, multiple, ce = True):
  # ltp is the last trading price
  # ce flag checks whether it is call or put
  # multiple indicates the lowest multiple in which strike prices are given
  if(ce==True):
    return int(math.ceil(ltp / multiple)) * multiple
  else:
    return int(math.ceil(ltp / multiple)) * multiple - multiple 

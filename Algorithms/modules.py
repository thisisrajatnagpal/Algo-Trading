# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 21:18:17 2023

@author: rajat
"""
from packages import *

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
            
def gen_dates(first_date, days):
    duration = dt.timedelta(days)
    from_date = dt.datetime.strptime(first_date, '%d-%m-%Y')
    #print(from_date.strftime("%A"))
    store = []
    for d in range(duration.days + 1):
        day = from_date + dt.timedelta(days=d)
        store.append(day)
    return store

def Modify_SL_Order(order_df, order_type = "buy", sl_per = 7):  
    # We have to get the options ticker in order to proceed with the function
    symbol = order_df['tradingsymbol'].iloc[0]
    # getting last traded price of the ticker from the API, please note that in order to get the last traded price of an options symbol, we have to add the prefix "NFO:"
    ltp = kite.ltp("NFO:" + symbol)["NFO:" + symbol]['last_price']

    # getting the stop loss based on the current traded price of the options ticker
    # leaving first variable out because we just need the stop loss price
    _, new_sl_price = util_get_price(ltp, order_type, sl_per)
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

def instrumentLookup(instrument_df, symbol):
    try:
        return instrument_df[instrument_df['tradingsymbol']==symbol]['instrument_token'].values[0]
    except:
        return -1
    
def fetch_OHLC(ticker, interval, from_date, to_date):
    """extracts historical data and outputs in the form of dataframe"""
    # tikcer is the NSE instrument you want to use
    # interval is the candlestick time frame for OHLC data
    # The dates should be in this form - "day-month-Year"
    instrument = instrumentLookup(instrument_df, ticker)
    from_date = dt.datetime.strptime(from_date, '%d-%m-%Y')
    to_date = dt.datetime.strptime(to_date, '%d-%m-%Y')
    data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    while True:
        if from_date.date() >= dt.date.today()-dt.timedelta(100):        
            data = data.append(pd.DataFrame(kite.historical_data(instrument, from_date, to_date, interval)))
            break
        else:
            to_date = from_date + dt.timedelta(100)
            data = data.append(pd.DataFrame(kite.historical_data(instrument, from_date, to_date, interval)))
            from_date = to_date
    data.set_index("date", inplace=True)
    return data

""" Or you can use the below function if you just want the latest OHLC Data from a certain date"""

def util_fetch_OHLC(ticker, interval, duration, instrument_df = instrument_df):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(), interval))
    data.set_index("date",inplace=True)
    return data


def Place_Order_with_trailing_SL_and_target(symbol, quantity, order_type="buy", sl_per=7, rr=None):
    if (order_type == "buy"):
        # If we are buing an option then the stop loss order will be selling the option
        t_type = kite.TRANSACTION_TYPE_BUY
        t_type_sl = kite.TRANSACTION_TYPE_SELL
        t_type_target = kite.TRANSACTION_TYPE_SELL
    elif (order_type == "sell"):
        # If we are selling an option then stop loss order will be buying the option
        t_type = kite.TRANSACTION_TYPE_SELL
        t_type_sl = kite.TRANSACTION_TYPE_BUY
        t_type_target = kite.TRANSACTION_TYPE_BUY

    # getting last traded price of the ticker from the API, please note that in order to get the last traded price of an options symbol, we have to add the prefix "NFO:"
    ltp = kite.ltp("NFO:" + symbol)["NFO:" + symbol]['last_price']

    # limit price and stop loss price will be adjusted according to the order type, the methodology is written in the utility function
    limit_price, sl_price, target_price = util_get_price(ltp, order_type, sl_per)

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
            a += 1
    for order in order_list:
        if order["order_id"] == limit_order:
            # Check for our order
            if order["status"] == "COMPLETE":
                # Check if our order is complete
                # if the order type is buy then the trigger price for the stop loss order is slightly higher than the stop loss price
                if (order_type == "buy"):
                    tp = round((1 + 0.01) * sl_price, 1)

                # if the order type is sell then the trigger price for the stop loss order is slightly lower than the stop loss price
                elif (order_type == "sell"):
                    tp = round((1 - 0.01) * sl_price, 1)

                # placing the stop loss order
                kite.place_order(tradingsymbol=symbol,
                                 exchange=kite.EXCHANGE_NFO,
                                 transaction_type=t_type_sl,
                                 quantity=quantity,
                                 order_type=kite.ORDER_TYPE_SL,
                                 price=sl_price,
                                 trigger_price=tp,
                                 product=kite.PRODUCT_MIS,
                                 variety=kite.VARIETY_REGULAR)

                if (target_price != None):
                    # placing the target order
                    kite.place_order(tradingsymbol=symbol,
                                     exchange=kite.EXCHANGE_NFO,
                                     transaction_type=t_type_target,
                                     quantity=quantity,
                                     order_type=kite.ORDER_TYPE_LIMIT,
                                     price=(target_price),
                                     product=kite.PRODUCT_MIS,
                                     variety=kite.VARIETY_REGULAR)

            else:
                kite.cancel_order(order_id=limit_order, variety=kite.VARIETY_REGULAR)


def cancel_sl_target(symbol, order_df):
    if(order_df.shape[0] == 0): return
    order_df_symbol = order_df.loc[(ord_df['tradingsymbol'].str.contains(symbol)) & (ord_df['status'].isin(["TRIGGER PENDING","OPEN"]))]
    if(order_df_symbol.shape[0] == 0): return
    for iter in order_df_symbol['order_id']:
        kite.cancel_order(order_id=iter, variety=kite.VARIETY_REGULAR)

def convertstrtodate(text):
    return dt.datetime.strptime(text, '%d-%m-%Y').date() 

# For stock options, it is fairly simple and scalable. This function should work for all NIFTY 50 stocks
def util_get_options_symbol(ticker, ltp):
    # Taking the rows from NFO DataFrame which contains the ticker name
    print(ticker)
    print(ltp)
    temp = NFO_instrument_df[NFO_instrument_df['tradingsymbol'].str.contains(ticker)]
    # Filtering out current month's options data
    temp  = temp[temp['tradingsymbol'].str.contains(dt.datetime.now().strftime("%B").upper()[0:3])]
    # Removing Futures type objects
    temp = temp[temp[ 'instrument_type'] != 'FUT']
    # Hard Coded the difference in strike price, change this part of the code if you are getting problems
    diff = temp['strike'].iloc[2] - temp['strike'].iloc[0]
    # getting the rounded off strike price based on the difference in strike price and the last trading price
    # CE strike price is taken as the closest upper "out of the money" options strike price
    ce_strike = util_util_get_strike_price(ltp, diff)
    #print(ce_strike)
    # PE strike price is taken as the closest lower "out of the money" strike price
    pe_strike = int(ce_strike - diff)
    #print(str(ce_strike) + "CE")
    #print(temp[temp['tradingsymbol'].str.contains(str(ce_strike) + "CE")])
    ce_df = temp[temp['tradingsymbol'].str.contains(str(ce_strike) + "CE")]
    #print(ce_df.iloc[0]['tradingsymbol'])
    #print(type(ce_df.iloc[0]['tradingsymbol']))
    pe_df = temp[temp['tradingsymbol'].str.contains(str(pe_strike) + "PE")]
    # returning the CE and PE symbol
    return ce_df.iloc[0]['tradingsymbol'], pe_df.iloc[0]['tradingsymbol'], ce_df.iloc[0]['lot_size']


def util_get_price(ref, order_type="buy", sl_per=7, rr=None):
    if (order_type == "buy"):
        # The order is a buy order, stop loss price is 7 percent less than the limit price
        # We have to set the limit price a little higher than the market price to get the order executed
        limit_price = ref * (1 + 0.005)
        sl_price = (1 - sl_per / 100) * limit_price
        if (rr != None):
            target_price = (1 + rr * sl_per / 100) * limit_price
            return round(limit_price, 1), round(sl_price, 1), round(target_price, 1)
        else:
            target_price = None
        return round(limit_price, 1), round(sl_price, 1), target_price

    elif (order_type == "sell"):
        # The order is a sell order, stop loss price is 7 percent higher than the limit price
        # We have to set the limit price a little lower to get the order executed
        limit_price = ref * (1 - 0.005)
        sl_price = (1 + sl_per / 100) * limit_price
        if (rr != None):
            target_price = (1 - rr * sl_per / 100) * limit_price
            return round(limit_price, 1), round(sl_price, 1), round(target_price, 1)
        else:
            target_price = None
        return round(limit_price, 1), round(sl_price, 1), target_price

def util_util_get_strike_price(ltp, multiple, ce = True):
  # ltp is the last trading price
  # ce flag checks whether it is call or put
  # multiple indicates the lowest multiple in which strike prices are given
  if(ce==True):
    return int(math.ceil(ltp / multiple)) * multiple
  else:
    return int(math.ceil(ltp / multiple)) * multiple - multiple 

def get_levels(df):
    supports = df[df.low == df.low.rolling(5, center = True).min()].low
    resistances = df[df.high == df.high.rolling(5, center = True).max()].high
    levels = pd.concat([supports, resistances])
    threshold = levels.mean()*0.0005
    levels = levels[abs(levels.diff() > 2)]
    return levels

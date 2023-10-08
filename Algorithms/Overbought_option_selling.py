# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 21:59:31 2023

@author: rajat
"""

from modules import *


def overbought_option_selling(df):
    custom_a = ta.Strategy(name="A", ta=[{"kind": "rsi"}])
    df.ta.strategy(custom_a)
    levels = get_levels(df)
    closest_value = min(levels.to_list(), key=lambda x: abs(df['close'].iloc[-2] - x))
    is_at_sup_res = abs(df['close'].iloc[-2] - closest_value) / df['close'].iloc[-2]
    is_at_sup_res = is_at_sup_res * 100
    check_volume = False
    if df['volume'].iloc[-2] < df['volume'].iloc[-3] < df['volume'].iloc[-4]:
        check_volume = True

    if is_at_sup_res < 0.06 and df['RSI_14'].iloc[-2] > 80 and check_volume is True:
        return True
    else:
        return False


def main(capital_):
    if kite.margins()['equity']['available']['opening_balance'] - kite.margins()['equity']['available']['live_balance'] > capital_:
        return
    a, b = 0, 0
    while a < 10:
        # running the loop multiple times to increase the probability of getting the required information in case if
        # connection is not established in one go
        try:
            # getting the open positions of the day
            pos_df = pd.DataFrame(kite.positions()["day"])
            break
        except:
            print("can't extract position data..retrying")
            a += 1
    while b < 10:
        # running the loop multiple times to increase the probability of getting the required information in case if
        # connection is not established in one go
        try:
            # getting the list of orders placed on the current day
            ord_df = pd.DataFrame(kite.orders())
            break
        except:
            print("can't extract order data..retrying")
            b += 1
    Open_SL_Orders = ord_df.loc[((ord_df['order_type'] == "SL") & (ord_df['status'] == "OPEN"))]
    if Open_SL_Orders.shape[0] != 0:
        Close_SL_Order(Open_SL_Orders)
    for ticker in tickers:
        print("starting pass through for.....", ticker)
        try:
            # last traded price of the NSE ticker stock
            ltp = kite.ltp("NSE:" + ticker)["NSE:" + ticker]['last_price']

            # currently quantity is set to one lot per options ticker, it can be changed in util_get_options_symbol
            # function
            ce_symbol, pe_symbol, quantity = util_get_options_symbol(ticker, ltp)
            open_position = False

            df = modules.fetchOHLC(ticker, "5minute", 2)

            if pos_df.shape[0] != 0:
                # if there is an open position
                if pos_df[pos_df['tradingsymbol'].str.contains(ticker)].shape[0] != 0:
                    open_position = True

            if not open_position:
                cancel_sl_target(ticker, ord_df)
                # Give some condition here
                if overbought_option_selling(df):
                    Place_Order_with_trailing_SL_and_target(ce_symbol, quantity, "sell", sl_per=7)
            if open_position:
                order_df = ord_df.loc[(ord_df['tradingsymbol'].str.contains(ticker)) & (
                    ord_df['status'].isin(["TRIGGER PENDING"]))]
                Modify_SL_Order(order_df, order_type)
        except:
            print("API error for ticker :", ticker)


if __name__ == '__main__':
    capital = 200000
    tickers = NFO_list
    starttime = time.time()
    timeout = pd.Timestamp(dt.date.today()) + pd.Timedelta('0 days 15:10:0.0000')
    x = pd.Timestamp(dt.date.today()) + pd.Timedelta('0 days 09:20:0.0000')
    x = dt.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S")
    while time.time() <= timeout:
        if time.time() >= x.timestamp():
            try:
                print("*************************************************")
                print("The Time is :", dt.datetime.fromtimestamp(time.time()))
                main(capital)
                time.sleep(60 * 5 - ((time.time() - starttime) % 60.0))
            except KeyboardInterrupt:
                print('\n\nKeyboard exception received. Exiting.')
                exit()

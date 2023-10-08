

# Importing required libraries
from kiteconnect import KiteConnect
import os
import datetime as dt
import pandas as pd
import numpy as np
import time
import math
import sys

#cwd = os.chdir("D:\Algo Trading")
sys.path.append("D:\Algo Trading")
import modules
import global_ as g
# Giving the path to the current working directory

# Generate trading session
access_token = open("D:/Algo Trading/access_token.txt",'r').read()
key_secret = open("D:/Algo Trading/api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)
Nifty_list = pd.read_csv("D:/Algo Trading/ind_nifty50list.csv")

# Get dump of all NSE/NFO Instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
instrument_df = instrument_df[instrument_df['name'] != ""]
instrument_df = instrument_df[instrument_df['tradingsymbol'].isin(Nifty_list['Symbol'].to_list())]
NFO_instrument_df = pd.DataFrame(kite.instruments("NFO"))
tickers = list(Nifty_list['Symbol'])


def main(capital):
    if(kite.margins()['equity']['available']['opening_balance'] - kite.margins()['equity']['available']['live_balance'] > capital): return
    a,b = 0,0
    while a < 10:
    # running the loop multiple times to increase the probability of getting the required information in case if connection is not eastablished in one go
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
    for ticker in tickers:
        print("starting passthrough for.....",ticker)    
        try:
            global flag, ltp
            ohlc = modules.fetchOHLC(ticker,"5minute",4)
            ohlc["st1"] = modules.supertrend(ohlc,7,3)
            ohlc["st2"] = modules.supertrend(ohlc,10,3)
            ohlc["st3"] = modules.supertrend(ohlc,11,2)

            # find this function in "python functions" folder in the same repository
            # It checks whether the trend is reversed or not, i.e., it checks wether all three supertrends have changed colour
            modules.st_dir_refresh(ohlc, ticker)
            print(g.st_dir[ticker])
            #quantity = # Using some notion, you have to decide how much quantity you want to trade for a particular stock based on the lot size for that particular stock
            ltp = kite.ltp("NSE:" + ticker)["NSE:" + ticker]['last_price']

            
            order_present = False
            
            if(pos_df.shape[0] != 0):
                # if there is an open position
                if(pos_df[pos_df['tradingsymbol'].str.contains(ticker)].shape[0] != 0):    
                    order_present = True
                
            
            if (not(order_present)):
                ce_symbol, pe_symbol, quantity = modules.get_options_symbol(ticker, ltp)
                # the code will execute only if there is no open position for the particular tickers and symbols
                if g.st_dir[ticker] == ["green","green","green"]:
                    modules.placeSLOrder(ce_symbol, quantity)
                if g.st_dir[ticker] == ["red","red","red"]:
                    modules.placeSLOrder(pe_symbol, quantity)
            if(order_present):
                order_df = ord_df.loc[(ord_df['tradingsymbol'].str.contains(ticker)) & (ord_df['status'].isin(["TRIGGER PENDING","OPEN"]))]
                modules.ModifyOrder(order_df)    
        except:
            print("API error for ticker :",ticker)
    

# tickers to track - recommended to use max movers from previous day
capital = 50000 # position size
#g.st_dir = {} # directory to store super trend status for each ticker
for ticker in tickers:
    g.st_dir[ticker] = ["None" ,"None", "None"]      
starttime=time.time()
timeout = pd.Timestamp(dt.date.today()) + pd.Timedelta('0 days 15:10:0.0000')
x = pd.Timestamp(dt.date.today()) + pd.Timedelta('0 days 09:20:0.0000')
x = dt.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S")
while time.time() <= timeout:
    if(time.time() >= x.timestamp()):
        try:
            print("*************************************************")
            print("The Time is :", dt.datetime.fromtimestamp(time.time()))
            main(capital)
            time.sleep(60 - ((time.time() - starttime) % 60.0))
        except KeyboardInterrupt:
            print('\n\nKeyboard exception received. Exiting.')
            exit()        
             

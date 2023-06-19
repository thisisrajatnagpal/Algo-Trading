from kiteconnect import KiteConnect
import logging
import os
import datetime as dt
import pandas as pd

cwd = os.chdir("Current Workinf Directory")

# generate trading sesion
# Please go to Gen Access folder to get these two files as input
access_token = open("access_token.txt", 'r').read()
key_secret = open("api_key.txt", 'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)
                 

# get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
instrument_df.to_csv("NSE_Instruments.csv", index = False)

def instrumentLookup(instrument_df, symbol):
    try:
        return instrument_df[instrument_df['tradingsymbol']==symbol]['instrument_token'].values[0]
    except:
        return -1
    
def fetchOHLC(ticker, interval, from_date, to_date):
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

def fetchOHLC(ticker, interval, duration, instrument_df = instrument_df):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(), interval))
    data.set_index("date",inplace=True)
    return data

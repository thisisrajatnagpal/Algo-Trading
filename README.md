# Algo-Trading
This repository contains the code snippets used for trading with Zerodha KiteConnect API using python
<p align="center">
  <img width="460" height="300" src="[http://www.fillmurray.com/460/300](https://user-images.githubusercontent.com/48415329/235424597-b8c761a7-63f4-47d8-b06a-75b2d3ee6800.png)">
  ![Kite](https://user-images.githubusercontent.com/48415329/235424597-b8c761a7-63f4-47d8-b06a-75b2d3ee6800.png)
</p>
<p align="center">
  <h4 align="center">A Hub of necessary python functions to use for algorithmic trading</h4>
</p>


<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>


## How To Use

To use the functions, you'll need to write the following code beforehand.
```bash
from kiteconnect import KiteConnect
import logging
import os
import datetime as dt
import pandas as pd

cwd = os.chdir("Current Working Directory")

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
```

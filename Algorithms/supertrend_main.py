def main(capital):
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
            ohlc = fetchOHLC(ticker,"5minute",4)
            ohlc["st1"] = supertrend(ohlc,7,3)
            ohlc["st2"] = supertrend(ohlc,10,3)
            ohlc["st3"] = supertrend(ohlc,11,2)

            # find this function in "python functions" folder in the same repository
            # It checks whether the trend is reversed or not, i.e., it checks wether all three supertrends have changed colour
            st_dir_refresh(ohlc, ticker)

            quantity = # Using some notion, you have to decide how much quantity you want to trade for a particular stock based on the lot size for that particular stock
            ltp = kite.ltp("NSE:" + ticker)["NSE:" + ticker]['last_price']

            ce_symbol, pe_symbol = get_options_symbol(ticker, ltp)
            order_present = False
            
            if(pos_df.shape[0] != 0):
                # if there is an open position
                if(pos_df[pos_df['tradingsymbol'].str.contains(ticker)].shape[0] != 0):    
                    order_present = True
                

            if (not(order_present)):
                # the code will execute only if there is no open position for the particular tickers and symbols
                if st_dir[ticker] == ["green","green","green"]:

                    placeSLOrder(ce_symbol, quantity)
                if st_dir[ticker] == ["red","red","red"]:
                    placeSLOrder(pe_symbol, quantity)
            if(order_present):
                order_id = ord_df.loc[(ord_df['tradingsymbol'].str.contains(ticker)) & (ord_df['status'].isin(["TRIGGER PENDING","OPEN"]))]
                ModifyOrder(order_id)    
        except:
            print("API error for ticker :",ticker)
    
tickers = # give the list of tickers here

# tickers to track - recommended to use max movers from previous day
capital = 15000 # position size
st_dir = {} # directory to store super trend status for each ticker
for ticker in tickers:
    st_dir[ticker] = ["None" ,"None", "None"]      
starttime=time.time()
timeout = time.time() + 60*60*2  # 60 seconds times 360 meaning 6 hrs
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
             

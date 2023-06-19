# For stock options, it is fairly simple and scalable. This function should work for all NIFTY 50 stocks
def get_options_symbol(ticker, ltp):
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
    ce_strike = get_strike_price(ltp, diff)
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

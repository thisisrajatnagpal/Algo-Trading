# For stock options, it is fairly simple and scalable. This function should work for all NIFTY 50 stocks

def get_options_symbol(ticker, ltp):
    ce_strike = get_strike_price(ltp, 100)
    pe_strike = ce_strike - 100
    temp = NFO_instrument_df[NFO_instrument_df['tradingsymbol'].str.contains(ticker)]
    temp  = temp[temp['tradingsymbol'].str.contains(dt.datetime.now().strftime("%B").upper())]
    ce_df = temp[temp['tradingsymbol'].str.contains(str(ce_strike) + "CE")]
    pe_df = temp[temp['tradingsymbol'].str.contains(str(pe_strike) + "PE")]
    return ce_df['tradingsymbol'].iloc[0], pe_df['tradingsymbol'].iloc[0]

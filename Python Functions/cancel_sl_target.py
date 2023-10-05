def cancel_sl_target(symbol, order_df):
    if(order_df.shape[0] == 0): return
    order_df_symbol = order_df.loc[(ord_df['tradingsymbol'].str.contains(symbol)) & (ord_df['status'].isin(["TRIGGER PENDING","OPEN"]))]
    if(order_df_symbol.shape[0] == 0): return
    for iter in order_df_symbol['order_id']:
        kite.cancel_order(order_id=iter, variety=kite.VARIETY_REGULAR)

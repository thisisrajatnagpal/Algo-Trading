

def MACD(DF, a, b, c):
    """function to calculate the MACD"""
  
    # a refers to Fast Moving Average
    # b refers to slow moving average
    # c refers to signal moving average
    df = DF.copy()
    df["MA_fast"] = df['close'].ewm(span=a, min_periods = a).mean()
    df['MA_slow'] = df['close'].ewm(span=b, min_periods = b).mean()
    df['MACD'] = df["MA_fast"]  - df["MA_slow"]
    df["Signal"] = df["MACD"].ewm(span=c, min_periods = c).mean()
    df.dropna(inplace=True)
    return df
  
  
def bollBnd(DF, n):
    """function to calculate the Bollinger Band"""
    
    # n refers to the moving average
    # bollinger band takes simple moving average
    df = DF.copy()
    df["MA"] = df['close'].rolling(n).mean()
    df["BB_up"] = df["MA"] + 2*df["close"].rolling(n).std(ddof=0)
    df["BB_dn"] = df["MA"] - 2*df["close"].rolling(n).std(ddof=0)
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df 

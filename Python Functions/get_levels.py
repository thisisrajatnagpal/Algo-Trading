def get_levels(df):
    supports = df[df.low == df.low.rolling(5, center = True).min()].low
    resistances = df[df.high == df.high.rolling(5, center = True).max()].high
    levels = pd.concat([supports, resistances])
    threshold = levels.mean()*0.0005
    levels = levels[abs(levels.diff() > 2)]
    return levels

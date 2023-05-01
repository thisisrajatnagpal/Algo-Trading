 """ Maticalgos library has past weekly expiry options data for Nifty and Banknifty"""
from maticalgos.historical import historical
ma = historical('Registered email ID')
ma.login("password")

# ins is the name if the instrument, i.e., "banknifty" or "nifty"
options_data = ma.get_data(ins, timestamp.date())


# This function generates the symbol for the desired strike price based on above generated data

# Here, price is the strike price you want to use
# Call_put is a string,  it can take value "CE" or "PE". Default is "CE"
def get_options_symbol(options_data, price, call_put = "CE"):
    substr = str(price) + call_put
    for iter in options_data['symbol']:
      # To check the presence of a substring in a string
        if(substr in iter):
            return iter

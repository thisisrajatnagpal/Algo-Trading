 """ Maticalgos library has past weekly expiry options data for Nifty and Banknifty"""
from maticalgos.historical import historical
ma = historical('Registered email ID')
ma.login("password")

# ins is the name if the instrument, i.e., "banknifty" or "nifty"
options_data = ma.get_data(ins, timestamp.date())


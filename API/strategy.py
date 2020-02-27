from utils import *
from tdapi import *
from trader import Trader

class Strategy():
	def __init__(self):
		self.data = get_recent_data(symbol,period_type,period,freq_type,freq,local=True)
		self.data = timestamp_to_iso(data)
		self.sma1 = sma(data,period1,'close')
		self.sma2 = sma(data,period2,'close')
		self.sma3 = sma(data,period3,'close')
		trade = Trader(self.data,100000)

	def strategy(self):
		if self.sma1 
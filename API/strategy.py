from utils import *
from data import *
from graph import candle
# from trader import Trader

class Strategy():
	def __init__(self,data):
		period1 = 10
		period2 = 50
		# period3 = 150
		self.data = data
		self.sma1 = sma(self.data,period1,'close')
		self.sma2 = sma(self.data,period2,'close')
		# self.sma3 = sma(self.data,period3,'close')

	def strategy(self,index):
		sma1,sma2 = self.sma1[index],self.sma2[index]
		if sma1 < sma2:
			self.trader.sell(10000)
		elif sma1 > sma2:
			self.trader.buy(10000)

	def run(self):
		for i in self.data.iterrows():
			self.strategy(i[0])

		candle(self.data,self.sma1,self.sma2,sell=sell,buy=buy)

	def add_trader(self,trader):
		self.trader = trader

# and sma1 < sma3 and sma2 < sma3
 # and sma1 > sma3 and sma2 > sma3
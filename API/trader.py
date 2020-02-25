from tdapi import get_recent_data
from utils import timestamp_to_iso
# from strategy import Strategy
from graph import candle

class Trader():
	def __init__(self,data,icash):
		self.data = data
		self.icash = icash
		self.ccash = icash
		self.value = 0
		print(self.data)

	def run(self):
		for index,row in self.data.iterrows():
			print(row['close'])

	def add_strategy(self,strategy):
		self.strategy = strategy
		print(self.strategy.response)

	def buy(self,amount):
		self.ccash -= amount
		self.value += amount

	def sell(self,amount):
		self.ccash += amount
		self.value -= amount


# data = get_recent_data('QQQ','month',6,'daily',1)
# data = timestamp_to_iso(data)

# trade = Trader(data,100000)
# trade.add_strategy(Strategy(data))
# print(data)
from utils import *
from trader import Trader

class Strategy():
	def __init__(self,data):
		self.data = sma(data,10,'close')
		self.response = 'buy'
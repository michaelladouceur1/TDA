class Trader():
	def _check_cash(func):
		def inner(self,*args):
			if self.ccash > 0:
				func(self,*args)
			else:
				return
		return inner

	def _check_value(func):
		def inner(self,*args):
			if self.value > 0:
				func(self,*args)
			else:
				return
		return inner

	def __init__(self,data,icash):
		self.data = data
		self.icash = icash
		self.ccash = icash
		self.value = 0
		print(self.data)

	def add_strategy(self,strategy):
		self.strategy = strategy
		print(self.strategy)

	@_check_cash
	def buy(self,amount=None):
		if amount is None:
			self.value = self.ccash
			self.ccash = 0
		else:
			self.ccash -= amount
			self.value += amount

	@_check_value
	def sell(self,amount=None):
		self.ccash += amount
		self.value -= amount


from data import get_recent_data, save_local_data
from tdapi import get_account_data
from utils import sma, timestamp_to_iso, crossover
from graph import candle
from strategy import Strategy
from trader import Trader

period1 = 10
period2 = 50
period3 = 150

symbol = 'QQQ'
periodType = 'day'
period = 10
freqType = 'minute'
freq = 1


data = get_recent_data(symbol,periodType,period,freqType,freq,local=True)
trader = Trader(data,100000)
strat = Strategy(data)
print(f'Cash: {trader.ccash}')
print(f'Value: {trader.value}')
strat.add_trader(trader)
strat.run()
print(f'Cash: {trader.ccash}')
print(f'Value: {trader.value}')
# strat = Strategy(symbol,period_type,period,freq_type,freq)
# print(strat.icash)

# def buy(dat,*args):
# 	return dat['datetime'][arg for arg in args]

# data = get_recent_data(symbol,period_type,period,freq_type,freq,local=True)
# data = timestamp_to_iso(data)
# print(data)
# sma1 = sma(data,period1,'close')
# sma2 = sma(data,period2,'close')
# sma3 = sma(data,period3,'close')
# data[f'sma_{period1}'] = sma1
# data[f'sma_{period2}'] = sma2
# data[f'sma_{period3}'] = sma3
# data = crossover(data,[f'sma_{period1}',f'sma_{period2}',f'sma_{period3}'])
# sell = data['datetime'][(sma1<sma2) & (sma2<sma3) & (sma1<sma3)]
# buy = data['datetime'][(sma1>sma2) & (sma2>sma3) & (sma1>sma3)]
# def reduce_bs(data):
# 	hold = []
# 	for i,s in enumerate(data.index[:-1]):
# 		# print(sell.index[i+1]-sell.index[i])
# 		# print(sell[s])
# 		if i == 0:
# 			continue
# 		else:
# 			if data.index[i+1]-data.index[i] != 1:
# 				hold.append(data.index[i+1])
# 	return data[hold]

# def buysell(data,buy,sell,icash):
# 	for i,b in enumerate(buy):
# 		pass

# buy = reduce_bs(buy)
# sell = reduce_bs(sell)
# # buysell(data,buy,sell,10000)
# print('-------BUY-------')
# print(buy)
# print('-------SELL-------')
# print(sell)


# save_local_data(data,type='recent',symbol=symbol,periodType=period_type,period=period,frequencyType=freq_type,frequency=freq)
# print(f'{sys.getsizeof(data)/1000} KB')

# candle(data,sma1,sma2,sma3,sell=sell,buy=buy)

# data = get_price_history(symbol=symbol,periodType=period_type,period=period,frequencyType=freq_type,frequency=freq)
# print(data)

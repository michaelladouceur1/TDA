from data import get_recent_data, save_local_data
from tdapi import get_account_data

period1 = 10
period2 = 50
period3 = 150

symbol = 'QQQ'
period_type = 'day'
period = 2
freq_type = 'minute'
freq = 1

# def buy(dat,*args):
# 	return dat['datetime'][arg for arg in args]

data = get_recent_data(symbol,period_type,period,freq_type,freq,local=True)
print(data)
# sma1 = sma(data,period1,'close')
# sma2 = sma(data,period2,'close')
# sma3 = sma(data,period3,'close')
# # sell = data['datetime'][sma1 < sma2]
# # sell = buy(data,sma1<sma2,sma2<sma3)
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
		

# buy = reduce_bs(buy)
# sell = reduce_bs(sell)
# print(buy)
# print(sell)


# save_local_data(data,type='recent',symbol=symbol,periodType=period_type,period=period,frequencyType=freq_type,frequency=freq)
# print(f'{sys.getsizeof(data)/1000} KB')

# candle(data,sma1,sma2,sma3,sell=sell,buy=buy)

# data = get_price_history(symbol=symbol,periodType=period_type,period=period,frequencyType=freq_type,frequency=freq)
# print(data)

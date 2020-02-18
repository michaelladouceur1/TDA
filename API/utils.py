import pandas as pd

def convert_to_df(data,index=None):
	return pd.DataFrame(data,index=index)

def timestamp_to_iso(data):
	data['datetime'] = data['datetime'].apply(lambda x: pd.Timestamp(x, unit='ms'))
	return data

def sma(data,window,param,win_type=None):
	data[f'sma_{window}'] = data[param].rolling(window,win_type).mean()
	return data

def crossover(data,cross1,cross2):
	state = 'hold'
	for index,row in data.iterrows():
		if data.loc[index,cross1] >= data.loc[index,cross2] and state != 'buy':
			data.loc[index,'bsh'] = 'buy'
			state = 'buy'
		elif data.loc[index,cross1] < data.loc[index,cross2] and state != 'sell':
			data.loc[index,'bsh'] = 'sell'
			state = 'sell'
		else:
			data.loc[index,'bsh'] = 'hold'

	return data
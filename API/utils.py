import pandas as pd

def convert_to_df(data,index=None):
	return pd.DataFrame(data,index=index)

def timestamp_to_iso(data):
	data['datetime'] = data['datetime'].apply(lambda x: pd.Timestamp(x, unit='ms'))
	return data

def sma(data,window,param,win_type=None):
	data[f'sma_{window}'] = data[param].rolling(window,win_type).mean()
	return data

def crossover(data,graphs):
	prev_state = ''
	for i,row in data.iterrows():
		state = []
		for j,graph in enumerate(graphs[:-1]):
			if data.loc[i,graph] >= data.loc[i,graphs[j+1:]].any():
				state.append('sell')
			elif data.loc[i,graph] <= data.loc[i,graphs[j+1:]].any():
				state.append('buy')
			else:
				state.append('hold')

		if all(elem == 'buy' for elem in state) and prev_state != 'buy':
			data.loc[i,'bsh'] = 'buy'
			prev_state = 'buy'
		elif all(elem == 'sell' for elem in state) and prev_state != 'sell':
			data.loc[i,'bsh'] = 'sell'
			prev_state = 'sell'
		else:
			data.loc[i,'bsh'] = 'hold'
		

	return data

def maxmin(data,graph,period):
	state = 'hold'
	for index,row in data.iterrows():
		if index <= period:
			continue
		else:
			if (data.loc[index,graph]-data.loc[index-period,graph])/period > 0 and state != 'buy':
				data.loc[index,'bsh'] = 'buy'
				state = 'buy'
			elif (data.loc[index,graph]-data.loc[index-period,graph])/period < 0 and state != 'sell':
				data.loc[index,'bsh'] = 'sell'
				state = 'sell'
			else:
				data.loc[index,'bsh'] = 'hold'

	return data
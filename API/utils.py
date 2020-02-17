import pandas as pd

def convert_to_df(data,index=None):
	return pd.DataFrame(data,index=index)

def timestamp_to_iso(data):
	data['datetime'] = data['datetime'].apply(lambda x: pd.Timestamp(x, unit='ms'))
	return data

def sma(data,window,param,win_type=None):
	data[f'sma_{window}'] = data[param].rolling(window,win_type).mean()
	return data
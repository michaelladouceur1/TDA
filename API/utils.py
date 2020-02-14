import pandas as pd

def sma(data,window,param=None,win_type=None):
	if param == None:
		df = pd.DataFrame(data)
	else:
		df = pd.Series()
		s = 0
		for i in data:
			df.set_value(s,i[param])
			s += 1
	
	sma = df.rolling(window,win_type).mean()

	return sma
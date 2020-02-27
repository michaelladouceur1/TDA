import sys
from tdapi import get_price_history
from utils import timestamp_to_iso

if sys.platform == 'linux' or sys.platform == 'linux2':
	DATA_PATH = '../Data/'
elif sys.platform == 'win32':
	DATA_PATH = '..\\Data\\'

@timestamp_to_iso
def get_recent_data(
	symbol, 
	periodType, 
	period, 
	frequencyType, 
	frequency, 
	needExtendedHoursData='true', 
	local=False,
	):
	if local == True:
		data = search_local_data('recent', symbol, periodType,
								 period, frequencyType=frequencyType, frequency=frequency)
		if data is not None:
			print('Local Data Found')
			return data
		else:
			res = get_price_history(
					symbol,
					periodType=periodType,
					period=period,
					frequencyType=frequencyType,
					frequency=frequency,
					needExtendedHoursData=needExtendedHoursData)

			return res

	else:
		res = get_price_history(
					symbol,
					periodType=periodType,
					period=period,
					frequencyType=frequencyType,
					frequency=frequency,
					needExtendedHoursData=needExtendedHoursData)

		return timestamp_to_iso(res)


def get_period_data(symbol, frequencyType, frequency, startDate, endDate, needExtendedHoursData='true'):
	print('Connecting to API')
	res = get_price_history(
			symbol,
			startDate=startDate,
			endDate=endDate,
			frequencyType=frequencyType,
			frequency=frequency,
			needExtendedHoursData=needExtendedHoursData)

	return res

def search_local_data(type, symbol, periodType=None, period=None, startDate=None, endDate=None, frequencyType=None, frequency=None):
	filename = get_filename(type=type, symbol=symbol, periodType=periodType, period=period, startDate=startDate,
							endDate=endDate, frequencyType=frequencyType, frequency=frequency)
	try:
		print(f'Local Search: {filename}')
		data = pd.read_csv(filename)
		return data
	except:
		print('Local file not found')


def save_local_data(data, type, symbol, periodType=None, period=None, startDate=None, endDate=None, frequencyType=None, frequency=None):
	filename = get_filename(type=type, symbol=symbol, periodType=periodType, period=period, startDate=startDate,
							endDate=endDate, frequencyType=frequencyType, frequency=frequency)
	try:
		print(f'Local Save: {filename}')
		data.to_csv(filename)
	except:
		print(f'An error occured saving data')


def get_filename(type, symbol, periodType=None, period=None, startDate=None, endDate=None, frequencyType=None, frequency=None):
	if type == 'recent':
		return f'{DATA_PATH}{symbol}-{periodType}-{period}-{frequencyType}-{frequency}-R.csv'
	elif type == 'period':
		return f'{DATA_PATH}{symbol}-{startDate}-{endDate}-{frequencyType}-{frequency}-P.csv'
from config import *
from utils import *
from graph import *
import pandas as pd
import numpy as np
import requests
from requests.exceptions import HTTPError
import json
from datetime import datetime
import pprint
import sys

if sys.platform == 'linux' or sys.platform == 'linux2':
	DATA_PATH = '../Data/'
elif sys.platform == 'win32':
	DATA_PATH = '..\\Data\\'


def get_recent_data(symbol, periodType, period, frequencyType, frequency, needExtendedHoursData='false', local=False):
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

		return res


def get_period_data(symbol, frequencyType, frequency, startDate, endDate, needExtendedHoursData='false'):
	print('Connecting to API')
	res = get_price_history(
			symbol,
			startDate=startDate,
			endDate=endDate,
			frequencyType=frequencyType,
			frequency=frequency,
			needExtendedHoursData=needExtendedHoursData)

	return res


def log_error(error, msg):
	print(msg)
	print(error)


def search_local_data(type, symbol, periodType=None, period=None, startDate=None, endDate=None, frequencyType=None, frequency=None):
	filename = get_filename(type=type, symbol=symbol, periodType=periodType, period=period, startDate=startDate,
							endDate=endDate, frequencyType=frequencyType, frequency=frequency)
	try:
		print(f'Local Search: {filename}')
		data = pd.read_csv(filename)
		return data
	except:
		return


def save_local_data(data, type, symbol, periodType=None, period=None, startDate=None, endDate=None, frequencyType=None, frequency=None):
	filename = get_filename(type=type, symbol=symbol, periodType=periodType, period=period, startDate=startDate,
							endDate=endDate, frequencyType=frequencyType, frequency=frequency)
	try:
		print(f'Local Save: {filename}')
		data.to_csv(filename)
	except Error as err:
		log_error(err, 'Data could not be saved locally.')


def get_filename(type, symbol, periodType=None, period=None, startDate=None, endDate=None, frequencyType=None, frequency=None):
	if type == 'recent':
		return f'{DATA_PATH}{symbol}-{periodType}-{period}-{frequencyType}-{frequency}-R.csv'
	elif type == 'period':
		return f'{DATA_PATH}{symbol}-{startDate}-{endDate}-{frequencyType}-{frequency}-P.csv'


def get_price_history(symbol, periodType=None, period=None, frequencyType=None, frequency=None, startDate=None, endDate=None, needExtendedHoursData='false'):
	ph_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
	data = {
		'apikey': API_KEY,
		'periodType': periodType,
		'period': period,
		'frequencyType': frequencyType,
		'frequency': frequency,
		'startDate': startDate,
		'endDate': endDate,
		'needExtendedHoursData': needExtendedHoursData
	}
	
	try:
		print('Connecting to API')
		res = requests.get(ph_url,params=data) 
		res.raise_for_status()
	except HTTPError as http_error:
		log_error(http_error,'HTTP Error')
	else:
		print('Data Received')
		res = json.loads(res.content)['candles']
		res = convert_to_df(res)
		return res

def get_instruments(symbol,projection='fundamental'):
	ins_url = 'https://api.tdameritrade.com/v1/instruments'
	data = {
		'apikey': API_KEY,
		'symbol': symbol,
		'projection': projection
	}

	res = requests.get(ins_url,params=data)
	res = json.loads(res.content)[symbol]['fundamental']
	res = convert_to_df(res,range(1))
	res = res.T

	return res

def get_account_data(fields=''):
	acc_url = f'https://api.tdameritrade.com/v1/accounts/{ACCOUNT_ID}'
	data = {
		'apikey': API_KEY,
		'fields': fields
	}
	headers = {
		'Bearer': ACCESS_TOKEN
		# 'Authorization': REFRESH_TOKEN
	}

	res = requests.get(acc_url, params=data, headers=headers)

	return res.content

def get_movers(index,direction,change):
	mov_url = f'https://api.tdameritrade.com/v1/marketdata/${index}/movers'
	data = {
		'apikey': API_KEY,
		'direction': direction,
		'change': change
	}

	res = requests.get(mov_url, params=data)
	res = json.loads(res.content)

	return res

period1 = 10
period2 = 30
period3 = 100

symbol = 'QQQ'
period_type = 'day'
period = 1
freq_type = 'minute'
freq = 1

def buy(dat,expression):
	return dat['datetime'][expression]

data = get_recent_data(symbol,period_type,period,freq_type,freq,local=True)
data = timestamp_to_iso(data)
sma1 = sma(data,period1,'close')
sma2 = sma(data,period2,'close')
# sell = data['datetime'][sma1 < sma2]
sell = buy(data,sma1<sma2)
buy = data['datetime'][sma1 > sma2]
hold = []
for i,s in enumerate(sell.index[:-1]):
	# print(sell.index[i+1]-sell.index[i])
	# print(sell[s])
	if i == 0:
		continue
	else:
		if sell.index[i+1]-sell.index[i] != 1:
			hold.append(sell.index[i+1])
		
# print_all(sell)
print(hold)
sell = sell[hold]
print(sell)
# print_all(buy)
# print(sma)
# print(data)
# print(data)
# data = sma(data,period2,'close')
# data = sma(data,period3,'close')
# crossover(data,[f'sma_{period3}',f'sma_{period2}',f'sma_{period1}'])

# save_local_data(data,type='recent',symbol=symbol,periodType=period_type,period=period,frequencyType=freq_type,frequency=freq)
# print(f'{sys.getsizeof(data)/1000} KB')
candle(data,sma1,sma2,sell=sell)
# print(sma1)

# data = get_price_history(symbol=symbol,periodType=period_type,period=period,frequencyType=freq_type,frequency=freq)
# print(data)

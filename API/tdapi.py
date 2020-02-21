from config import *
from utils import *
from graph import *
import requests
import json
from datetime import datetime
import pprint
import sys 

pp = pprint.PrettyPrinter(indent=4)

def get_recent_data(symbol,periodType,period,frequencyType,frequency,needExtendedHoursData='false'):
    ph_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
    data = {
        'apikey': API_KEY,
        'periodType': periodType,
        'period': period,
        'frequencyType': frequencyType,
        'frequency': frequency
    }
    print(data)

    res = requests.get(ph_url,params=data)
    print(res)
    res = json.loads(res.content)['candles']
    res = convert_to_df(res)

    return res

def get_period_data(symbol,frequencyType,frequency,startDate,endDate,needExtendedHoursData='false'):
    ph_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
    data = {
        'apikey': API_KEY,
        'frequencyType': frequencyType,
        'frequency': frequency,
        'startDate': startDate,
        'endDate': endDate,
        'needExtendedHoursData': needExtendedHoursData
    }

    res = requests.get(ph_url,params=data)
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

data = get_recent_data(symbol,period_type,period,freq_type,freq)
data = timestamp_to_iso(data)
# print(data)
data = sma(data,period1,'close')
data = sma(data,period2,'close')
data = sma(data,period3,'close')
crossoverdiff(data,[f'sma_{period3}',f'sma_{period2}',f'sma_{period1}'])
# data = crossover(data,f'sma_{period1}',f'sma_{period2}')
# data = maxmin(data,f'sma_{period1}',20)
# with pd.option_context('display.max_rows', None):
#     print(data)
print(f'{sys.getsizeof(data)/1000} KB')
candle(data,f'sma_{period3}',f'sma_{period2}',f'sma_{period1}',bsh=True)
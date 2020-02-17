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

    res = requests.get(ph_url,params=data)
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

# data = get_recent_data('QQQ','year',3,'daily',1)
# data = timestamp_to_iso(data)
# # print(data)
# data = sma(data,30,'close')
# data = sma(data,15,'close')
# print(data)
# print(f'{sys.getsizeof(data)/1000} KB')
# candle(data,'sma_15','sma_30')
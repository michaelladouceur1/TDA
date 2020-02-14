from config import *
import requests
import json
from datetime import datetime
import pprint

pp = pprint.PrettyPrinter(indent=4)

def get_recent_data(symbol,periodType,period,frequencyType,frequency,needExtendedHoursData='false'):
    ph_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
    data = {
        'apikey': API_KEY,
        'periodType': periodType,
        'period': period,
        'frequencyType': frequencyType,
        'frequency': frequency,
        # 'endDate': endDate,
        # 'startDate': startDate,
        # 'needExtendedHoursData': needExtendedHoursData
    }

    res = requests.get(ph_url,params=data)

    return json.loads(res.content)['candles']

def get_period_data(symbol,frequencyType,frequency,endDate,startDate,needExtendedHoursData='false'):
    ph_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
    data = {
        'apikey': API_KEY,
        'frequencyType': frequencyType,
        'frequency': frequency,
        'endDate': endDate,
        'startDate': startDate,
        'needExtendedHoursData': needExtendedHoursData
    }

    res = requests.get(ph_url,params=data)

    return json.loads(res.content)['candles']

def get_instruments(symbol,projection='fundamental'):
    ins_url = 'https://api.tdameritrade.com/v1/instruments'
    data = {
        'apikey': API_KEY,
        'symbol': symbol,
        'projection': projection
    }

    res = requests.get(ins_url,params=data)

    return json.loads(res.content)[symbol]

# data = get_recent_data('GOOG','month',6,'daily',1)
# print(len(data))

# for i in data:
#     time = i['datetime']/1000
#     print(datetime.fromtimestamp(time).isoformat())
#     print(i)

data = get_instruments('FNV')
pp.pprint(data)
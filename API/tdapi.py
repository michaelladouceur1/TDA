from config import *
from utils import *
import requests
import json
from datetime import datetime
import pprint
import pandas

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
    res = pd.DataFrame(json.loads(res.content)['candles'])

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

	return json.loads(res.content)

data = get_recent_data('GOOG','month',2,'daily',1)
print(data)
print(type(data))
# sma = sma(data,10,'close')

# data.append(sma)
# print(type(sma))

# for i in data:
#     time = i['datetime']/1000
#     print(datetime.fromtimestamp(time).isoformat())
#     print(i)

# print(sma)

# data = get_instruments('FNV')
# pp.pprint(data)

# data = get_account_data()
# print(data)

# data = get_movers('SPX.X','up','percent')
# pp.pprint(data)
from config import *
from utils import convert_to_df
import requests
import json

BASE = 'https://api.tdameritrade.com/v1/'

def get_price_history(
	symbol, 
	periodType=None, 
	period=None, 
	frequencyType=None, 
	frequency=None, 
	startDate=None, 
	endDate=None, 
	needExtendedHoursData='false'
	):
	ph_url = f'{BASE}marketdata/{symbol}/pricehistory'
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

	res = requests.get(ph_url,params=data) 
	res = json.loads(res.content)['candles']
	res = convert_to_df(res)
	return res

def get_instruments(symbol,projection='fundamental'):
	ins_url = f'{BASE}instruments'
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
	acc_url = f'{BASE}accounts/{ACCOUNT_ID}'
	data = {
		'apikey': API_KEY,
		'fields': fields
	}
	headers = {
		'Authorization': f'Bearer {ACCESS_TOKEN}' 
		# 'Authorization': REFRESH_TOKEN
	}

	res = requests.get(acc_url, params=data, headers=headers)

	return res.content

def get_movers(index,direction,change):
	mov_url = f'{BASE}marketdata/${index}/movers'
	data = {
		'apikey': API_KEY,
		'direction': direction,
		'change': change
	}

	res = requests.get(mov_url, params=data)
	res = json.loads(res.content)

	return res
import requests
import json


def getTicker():
    url = 'https://b5cb0bbc.us-south.apigw.appdomain.cloud/stock_db/get_db_tickers'
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    json_data = json.loads(response.text)
    tickers = list(json_data.values())[0]
    return tickers

def getName():
    url = 'https://b5cb0bbc.us-south.apigw.appdomain.cloud/stock_db/get_db_names'
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    json_data = json.loads(response.text)
    names = list(json_data.values())[0]
    return names

def stockDB():
    tickers = getTicker()
    names = getName()
    stocks = {tickers[i]: names[i] for i in range(len(names))}
    return stocks

sectors = {'materials': 'basic-materials/', 'communications': 'communication-services/', 'discretionary': 'consumer-cyclical/', 'cyclical': 'consumer-cyclical/',
	 'staples': 'consumer-defensive/',
	 'defensive': 'consumer-defensive/',
	 'energy': 'energy/',
	 'financials': 'financial-services/',
	 'health care': 'healthcare/',
	 'industrials': 'industrials/',
	 'tech': 'technology/',
	 'utilities': 'utilities/'}

periods = {'1d': '1d','5d': '5d', '1m': '1mo', '3m': '3mo', '6m': '6mo', '1y': '1y', '2y': '2y', '3y': 756, '5y': '5y', '10y': '10y', 'ytd': 'ytd', 'max': 'max'}
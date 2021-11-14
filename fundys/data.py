from datetime import datetime
from datetime import timedelta
from time import time
from datetime import date
import pandas as pd
import numpy as np
import yfinance as yf
from bs4 import BeautifulSoup
import requests
from . import db
from tqdm import tqdm

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }
stocks = db.stockDB()
sectors = db.sectors
periods = db.periods

def nameForUrl(stockName):
    name = [v for k, v in stocks.items() if k == stockName][0]
    return name

def parseData(url, timeFrame):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('table', class_=['historical_data_table table'])
    time = [results[0] if timeFrame == "A" else results[1]]
    history = time[0].find_all('td')
    histList = [i.get_text() for i in history]
    yearsQuarters = [histList[i::2] for i in range(2)]
    change = [yearsQuarters[1][i].replace('$', '') for i in range(len(yearsQuarters[1]))]
    change = [c if len(c) > 0  else '0' for c in change]
    output = [int(change[i].replace(',', '')) for i in range(len(change))]
    return dict(zip(yearsQuarters[0], output))

def parseNoTime(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('table', class_=['historical_data_table table'])
    time = [results[0]]
    history = time[0].find_all('td')
    histList = [i.get_text() for i in history]
    yearsQuarters = [histList[i::2] for i in range(2)]
    change = [yearsQuarters[1][i].replace('$', '') for i in range(len(yearsQuarters[1]))]
    change = [c if len(c) > 0  else '0' for c in change]
    output = [int(change[i].replace(',', '')) for i in range(len(change))]
    final = dict(zip(yearsQuarters[0], output))
    return final

###### Income statement data

def getInventory(stockName,timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/inventory"
    final = parseData(url, timeFrame)
    return final

def getRevenue(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/revenue"
    final = parseData(url, timeFrame)
    return final

def getGrossProfit(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/gross-profit"
    final = parseData(url, timeFrame)
    return final

def getOperatingIncome(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/operating-income"
    final = parseData(url, timeFrame)
    return final

def getEbit(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/ebit"
    final = parseData(url, timeFrame)
    return final


def getEBITDA(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/ebitda"
    final = parseData(url, timeFrame)
    return final
    
def getInterest(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker + '/financials'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all('span')
    row = [t.get_text() for t in tables]
    dates = [row.index("Breakdown")+num for num in range(1,6)]
    date = [row[i] for i in dates]
    int_tables = soup.find_all('span')
    int_row = [t.get_text() for t in int_tables]
    ie = [int_row.index('Interest Expense')+num for num in range(1,6)]
    interests = [int_row[i] for i in ie]
    change = [i if len(i) > 0  else '0' for i in interests]
    interest = [c[:-3].replace(',', '') for c in change if "," in c]
    final_int = [int(i) for i in interest]
    return {date[i]: final_int[i] for i in range(len(final_int))}

def getNetIncome(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/net-income"
    final = parseData(url, timeFrame)
    return final
    
def getEPS(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/eps-earnings-per-share-diluted"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('table', class_=['historical_data_table table'])
    time = [results[0] if timeFrame == "A" else results[1]]
    history = time[0].find_all('td')
    histList = [i.get_text() for i in history]
    yearsQuarters = [histList[i::2] for i in range(2)]
    change = [yearsQuarters[1][i].replace('$', '') for i in range(len(yearsQuarters[1]))]
    change = [c if len(c) > 0  else '0' for c in change]
    output = [float(change[i].replace(',', '')) for i in range(len(change))]
    return dict(zip(yearsQuarters[0], output))

    
def getSharesOutstanding(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/shares-outstanding"
    final = parseData(url, timeFrame)
    return final
    
##### Balance sheet items

def getTotalAssets(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/total-assets"
    final = parseData(url, timeFrame)
    return final

def getCashOnHand(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/cash-on-hand"
    final = parseData(url, timeFrame)
    return final

def getLongTermDebt(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/long-term-debt"
    final = parseData(url, timeFrame)
    return final

def getTotalLiab(ticker, timeFrame):
    name = nameForUrl(ticker)
    url = "https://www.macrotrends.net/stocks/charts/" + ticker + "/" + name + "/total-liabilities"
    final = parseData(url, timeFrame)
    return final

def getShareholderEquity(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/total-share-holder-equity"
    final = parseData(url, timeFrame)
    return final
    
def getEmployees(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/number-of-employees"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('table', class_=['historical_data_table table'])
    time = [results[0]]
    history = time[0].find_all('td')
    histList = [i.get_text() for i in history]
    yearsQuarters = [histList[i::2] for i in range(2)]
    change = [yearsQuarters[1][i].replace('$', '') for i in range(len(yearsQuarters[1]))]
    output = [int(change[i].replace(',', '')) for i in range(len(change))]
    final = dict(zip(yearsQuarters[0], output))
    return final

def getCurrentAssets(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/total-current-assets"
    final = parseData(url, timeFrame)
    return final
    
def getCurrentLiab(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/total-current-liabilities"
    final = parseData(url, timeFrame)
    return final
    
def getPPE(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/net-property-plant-equipment"
    final = parseData(url, timeFrame)
    return final
    
def getRecievables(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/receivables-total"
    final = parseData(url, timeFrame)
    return final
    
def getPayables(ticker):
    url = 'https://www.zacks.com/stock/quote/' + ticker + '/balance-sheet'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    pay_tables = soup.find_all('td')
    tables = soup.find_all('span')
    row = [t.get_text() for t in tables]
    payRow = [t.get_text() for t in pay_tables]
    ap = [payRow.index('Accounts Payable')+num for num in range(1,6)]
    dates = [row.index("Liabilities & Shareholders Equity")+num for num in range(1,6)]
    payable = [payRow[i] for i in ap]
    date = [row[i] for i in dates[1:]]
    payables = [int(i.replace(',', '')) for i in payable[1:]]
    return {date[i]: payables[i] for i in range(len(payables))}

def getCOGS(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/cost-goods-sold"
    final = parseData(url, timeFrame)
    return final
    
def getOperatingExpenses(stock, timeFrame):
    operatingIncome = getOperatingIncome(stock, timeFrame)
    grossProfit = getGrossProfit(stock, timeFrame)
    operatingAnn = list(operatingIncome.values())
    grossAnn = list(grossProfit.values())
    opExpAnn = [grossAnn[i] - operatingAnn[i] for i in range(len(grossAnn))]
    years = list(grossProfit.keys())
    finalOpAnn = dict(zip(years, opExpAnn))
    return finalOpAnn

def getOperatingCF(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/cash-flow-from-operating-activities"
    final = parseNoTime(url)
    return final

def getInvestingCF(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/cash-flow-from-investing-activities"
    final = parseNoTime(url)
    return final

def getFinancingCF(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/cash-flow-from-financial-activities"
    final = parseNoTime(url)
    return final

def getDepreciation(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/total-depreciation-amortization-cash-flow"
    final = parseNoTime(url)
    return final

def getNetPPEchange(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/net-change-in-property-plant-equipment"
    final = parseNoTime(url)
    return final
    
def getNetCurrentDebt(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/net-current-debt"
    final = parseNoTime(url)
    return final
    
def getNetDebt(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/debt-issuance-retirement-net-total"
    final = parseNoTime(url)
    return final
    
def getTotalDivsPaid(stockName):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/total-common-preferred-stock-dividends-paid"
    final = parseNoTime(url)
    return final

def getTaxes(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/total-provision-income-taxes"
    final = parseData(url, timeFrame)
    return final

def getPretaxIncome(stockName, timeFrame):
    name = nameForUrl(stockName)
    url = "https://www.macrotrends.net/stocks/charts/"+ stockName + "/" + name + "/pre-tax-income"
    final = parseData(url, timeFrame)
    return final

def getCapex(ticker):
    ppe = list(getPPE(ticker, "A").values())
    ppeChange = [ppe[i] - ppe[i+1] for i in range(len(ppe)-1)]
    dep = list(getDepreciation('AAPL').values())
    years = list(getDepreciation('AAPL').keys())
    capex = [ppeChange[i] + dep[i] for i in range(len(ppeChange))]
    return {years[i]: capex[i] for i in range(len(capex))}

def fcf(ticker):
    ocf = list(getOperatingCF(ticker).values())
    interest = list(getInterest(ticker).values())
    taxes = list(getTaxes(ticker, "A").values())
    pretax = list(getPretaxIncome(ticker, "A").values())
    taxPerc = [taxes[i] / pretax[i] for i in range(len(taxes))]
    intertax = [interest[i] * (1-taxPerc[i]) for i in range(len(interest))]
    capex = list(getCapex(ticker).values())
    fcf = [ocf[i] + intertax[i] - capex[i] for i in range(len(intertax))]
    years = list(getOperatingCF(ticker).keys())
    return {years[i]: round(fcf[i], 2) for i in range(len(fcf))}

def price(stockName):
    url = "https://finance.yahoo.com/quote/" + stockName
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = list(soup.find('span', class_=["Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]))
    results = [results[0].replace(',', '')]
    return float(results[0])

def marketCap(ticker):
    p = price(ticker)
    shares = getSharesOutstanding(ticker, 'Q')
    return p * shares

def sectorTickers(sectorName):
    name = [v for k, v in sectors.items() if k == sectorName][0]
    url = "https://www.stockmonitor.com/sector/" + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('a', href=True)
    parsed = [r.get_text() for r in results]
    front = parsed[0:10]
    back = parsed[:-7]
    tickers = back[10:]
    return tickers

def prices(stock, start, end=None):
    if end == None:
        if start in periods.keys():
            period = [v for k, v in periods.items() if start == k][0]
            if period == 756:
                prices = yf.Ticker(stock).history('max')['Close']
                hist = prices[-period:]
                return pd.DataFrame(hist)
            else:
                prices = yf.Ticker(stock).history(period)['Close']
                return pd.DataFrame(prices)
        else:
            raise ValueError('invalid input: '  + start + '. Valid options are: 1d, 5d, 1m, 3m, 6m, 1y, 2y, 3y, 5y, 10y, ytd, max. Or add a finish date.')
    else:
        prices = list(yf.download(stock, start=start, end=end)['Adj Close'])
        return prices

def volume(stock, start, end=None):
    if end == None:
        if start in periods.keys():
            period = [v for k, v in periods.items() if start == k][0]
            if period == 756:
                volumes = yf.Ticker(stock).history('max')['Volume']
                hist = volumes[-period:]
                return pd.DataFrame(hist)
            else:
                volumes = yf.Ticker(stock).history(period)['Volume']
                return pd.DataFrame(volumes)
        else:
            raise ValueError('invalid input: '  + start + '. Valid options are: 1d, 5d, 1m, 3m, 6m, 1y, 2y, 3y, 5y, 10y, ytd, max. Or add a finish date.')
    else:
        volumes = list(yf.download(stock, start=start, end=end)['Volume'])
        return volumes

def sector(ticker):
    url = 'https://finance.yahoo.com/quote/'+ ticker + '/profile'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    find = soup.find_all('span', class_='Fw(600)')
    results = [f.get_text() for f in find]
    if len(results) == 0:
        find = soup.find_all('span', class_='Fl(end)')
        results = [f.get_text() for f in find]
        #sec = [results[0] if results[0] != "N/A" else results[1]]
        sec = results[5]
    else:
        sec = results[0]
    return sec

def industry(ticker):
    url = 'https://finance.yahoo.com/quote/'+ ticker + '/profile'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    find = soup.find_all('span', class_='Fw(600)')
    results = [f.get_text() for f in find]
    if len(results) == 0:
        find = soup.find_all('span', class_='Fl(end)')
        results = [f.get_text() for f in find]
        ind = [results[0] if results[0] != "N/A" else results[1]]
        ind = ind[0]
    else:
        ind = results[1]
    return ind

def optionExp(ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "/options"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all('option')
    values = [tag['value'] for tag in tables if "value" in tag.attrs]
    dates = [i.get_text() for i in tables]
    reference = dict(zip(dates, values))
    return reference

def optionExpry(ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "/options"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all('option')
    dates = [i.get_text() for i in tables]
    return dates

def callsPuts(ticker, date):
    reference = optionExp(ticker)
    table = [v for k, v in reference.items() if k == date][0]
    tableUrl = 'https://finance.yahoo.com/quote/' + ticker + '/options?date=' + table
    page = requests.get(tableUrl, headers=headers)
    test = pd.read_html(page.text)
    return test

def calls(ticker, date):
    calls = callsPuts(ticker, date)
    return calls[0]

def puts(ticker, date):
    puts = callsPuts(ticker, date)
    return puts[1]

def ttmDivs(ticker):
    divs = yf.Ticker(ticker).dividends
    today = date.today()
    yearAgo = today - timedelta(days=365)
    date_range = np.arange(yearAgo,today,dtype='datetime64[D]')
    divIndex = [divs.index[d] for d in range(len(divs)) if divs.index[d] in date_range]
    ttmdivs = [divs[p] for p in divIndex]
    return round(np.sum(ttmdivs), 2)

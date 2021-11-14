from scipy.stats import pearsonr
import yfinance as yf
import pandas as pd
import numpy as np
import itertools
from . import data
from . import ratios
from tqdm import tqdm
import matplotlib.pyplot as plt


vol_intervals = {'1w': 5 , '2w': 10, '1m': 21, '3m': 63, '6m': 126, '1y': 252, '3y': 756, '5y': 1260, 'max': True}
rollingReturnIntervals = {'1w': 5, '2w': 10, '1m': 21, '2m': 42, '3m': 63, '6m': 126}
deviationIntervals = {'1w': 52, '2w': 26, '1m': 12, '2m': 6, '3m': 4, '6m': 2}
portVolIntervals = {"Y": 1, "M": 12, "W": 52, "D": 252}

#Deviation (w list)
def deviation(prices, interval=None):
    if interval == None:
        df = pd.DataFrame(prices)
        dff = df.sort_index(ascending=True)
        pctChange = dff.pct_change()
        stddev = np.std(pctChange)
        dev = np.sqrt(252) * stddev
        return list(round(dev * 100, 2))[0]
    else:
        intv = [v for k, v in deviationIntervals.items() if interval == k][0]
        stddev = np.std(prices)
        dev = np.sqrt(intv) * stddev
        return round(dev * 100, 2)


def getcombos(stocks, maxStocks):
    for i in range(maxStocks,maxStocks+1):
        combs = itertools.combinations(stocks, i)
        return list(combs)

def stdDev(ticker, interval):
    time = [v for k, v in vol_intervals.items() if interval == k][0]
    history = list(yf.Ticker(ticker).history('max')['Close'])
    hist = [history if time == True else history[-time:]][0]
    series = pd.Series(hist)
    results = series.pct_change()
    stddev = np.std(results)
    return round(np.sqrt(252) * stddev, 4)

def returns(ticker, timeFrame, interval):
    prices = yf.Ticker(ticker).history(timeFrame)['Close']
    df = pd.DataFrame(prices)
    dff = [df if interval == "D" else df.resample(interval).apply(lambda x: x[-1])]
    return dff[0].pct_change()

def portReturns(portfolio, timeFrame, interval):
    prices = {p: list(yf.Ticker(p).history(timeFrame)['Close']) for p in portfolio}
    dates = [yf.Ticker(p).history(timeFrame)['Close'].index for p in portfolio]
    lengths = [len(v) for k, v in prices.items()]
    hist = -min(lengths)
    df = pd.DataFrame()
    df['Dates']= dates[0][hist:]
    for k, v in prices.items():
        df[k] = v[hist:]
    df = df.set_index('Dates')
    dff = [df if interval == "D" else df.resample(interval).apply(lambda x: x[-1])]
    return dff[0].pct_change()

def rollingReturns(ticker, timeFrame, interval):
    intv = [v for k, v in rollingReturnIntervals.items() if interval == k][0]
    hist = yf.Ticker(ticker).history(timeFrame)['Close']
    res = [round((hist[i + intv] / hist[i]) -1, 6) for i in range(len(hist)-intv)]
    return res

def rollingDev(ticker, timeFrame, interval):
    intv = [v for k, v in deviationIntervals.items() if interval == k][0]
    rolling = rollingReturns(ticker, timeFrame, interval)
    stddev = np.std(rolling)
    return round(np.sqrt(intv) * stddev, 4)
    
def portRollingDevs(port, period, interval):
    rolls = [rollingReturns(i, period, interval) for i in port]
    dev = [deviation(i, interval) for i in rolls]
    return {port[i]: dev[i] for i in range(len(port))}
    
def portVol(df, weights):
    cov = df.cov() * 252
    port_var = np.dot(np.transpose(weights), np.dot(cov, weights))
    return round(np.sqrt(port_var) * 100, 2)

def simpleReturnAndVol(portfolio, weights, timeFrame):
    df = portReturns(portfolio, timeFrame, "D")
    port_vol = portVol(df, weights, "D")
    simpleReturns = round(np.sum(df.mean() * weights * 252) * 100, 2)
    return {'Exp returns': simpleReturns, 'Volatility': port_vol}

def simpleReturn(portfolio, weights, timeFrame):
    df = portReturns(portfolio, timeFrame, "D")
    simpleReturns = df.mean() * weights * 252
    return simpleReturns

def portTTMdivs(portfolio):
    divs = [data.ttmDivs(p) for p in portfolio]
    return divs

def getYields(portfolio):
    yields = [ratios.divYield(p) for p in portfolio]
    return yields

def complexReturn(portfolio, weights):
    df = portReturns(portfolio, '1y', 'D')
    yields = getYields(portfolio)
    simpleReturns = df.mean() * weights * 252
    port = [yields[i] * weights[i] for i in range(len(weights))]
    final = np.sum([port[i] + simpleReturns[i] for i in range(len(simpleReturns))])
    return round(final * 100, 2)

def complexAndVol(portfolio, weights):
    comp = complexReturn(portfolio, weights)
    returns = portReturns(portfolio, '1y', 'D')
    vol = portVol(returns, weights)
    return {'Return:': comp, "Volatility:": vol}

def effecientFrontier(portfolio, tests):
    yields = getYields(portfolio)
    pctChanges = portReturns(portfolio, '1y', "D")
    cov_matrix = pctChanges.cov() * 252
    pret = []
    pvol = []
    pweights = []
    num_assets = len(portfolio)
    num_ports = tests
    for portfolio in tqdm(range(num_ports)):
        weight = np.random.random(num_assets)
        weight = weight/np.sum(weight)
        pweights.append(weight)
        returns = np.dot(weight, yields)
        pret.append(returns)
        varr = np.dot(np.transpose(weight), np.dot(cov_matrix, weight))
        sd = np.sqrt(varr)
        pvol.append(sd)
    data = {'Returns': pret, 'Volatility':pvol}
    for counter, symbol in enumerate(pctChanges.columns.tolist()):
        data[symbol+'weight'] = [w[counter] for w in pweights]
    portfolios = pd.DataFrame(data)
    return(portfolios)

def plotFrontier(frontier):
    frontier.plot.scatter(x='Volatility', y='Returns',color = 'r', marker='o', s=10, alpha=.3, grid=True, figsize=[10,10])

def highestReturnToRisk(frontier):
    num = 0
    rr_ratio = {}
    for v in tqdm(frontier['Volatility']):
        for r in frontier['Returns']:
            rr = r / v
            rr_ratio[v] = rr
            num = num + 1
    high = max(rr_ratio.values())
    voll = [k for k, v in rr_ratio.items() if v == high]
    return frontier.loc[frontier['Volatility'] == voll[0]]

def lowestVol(frontier):
    return frontier.iloc[frontier['Volatility'].idxmin()]

def highestReturn(frontier):
    return frontier.iloc[frontier['Returns'].idxmax()]

#Sector weighting
def sectorWeighting(portfolio, weights):
    sectors = [data.sector(p) for p in portfolio]
    weighting = {portfolio[s]: [sectors[s], weights[s]] for s in range(len(portfolio))}
    secWeight = {}
    for k, v in weighting.items():
        if list(v)[0] in secWeight:
            secWeight[v[0]].append(v[1])
        else:
            secWeight[v[0]] = [v[1]]
    final = {k: np.sum(v) for k, v in secWeight.items()}
    return final
#Plot sector weighting
def plotSectorWeighting(sectors):
    secnames = sectors.keys()
    secw = sectors.values()
    fig = plt.figure(figsize =(10, 10))
    plt.pie(secw, labels = secnames)
    plt.legend(sectors.values(), loc = 'lower right')
#Industry weighting
def industryWeighting(portfolio, weights):
    industries = [data.industry(p) for p in portfolio]
    weighting = {portfolio[s]: [industries[s], weights[s]] for s in range(len(portfolio))}
    indWeight = {}
    for k, v in weighting.items():
        if list(v)[0] in indWeight:
            indWeight[v[0]].append(v[1])
        else:
            indWeight[v[0]] = [v[1]]
    final = {k: np.sum(v) for k, v in indWeight.items()}
    return final
#Plot Industry weighting 
def plotIndustryWeighting(industries):
    indnames = industries.keys()
    indw = industries.values()
    fig = plt.figure(figsize =(10, 10))
    plt.pie(indw, labels = indnames)
    plt.legend(industries.values(), loc = 'lower right')

def portCreator(stocks, maxStocks):
    combs = getcombos(stocks, maxStocks)
    ports = [item for c in combs for item in c]
    portfolios = [ports[i:i + maxStocks] for i in range(0, len(ports), maxStocks)]
    return portfolios

def correl(stock1, stock2, timeFrame):
    stock1prices = list(yf.Ticker(stock1).history(timeFrame)['Close'])
    stock2prices = list(yf.Ticker(stock2).history(timeFrame)['Close'])
    return round(pearsonr(stock1prices, stock2prices)[0], 2)

def corrMatrix(port, timeFrame):
    prices = [list(yf.Ticker(p).history(timeFrame)['Close']) for p in port]
    df = pd.DataFrame()
    for i in range(len(port)):
        df[port[i]] = prices[i]
    return df.corr(method='pearson')

    

    return df
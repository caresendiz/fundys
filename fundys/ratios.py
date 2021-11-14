from datetime import date, timedelta
from . import data
import pandas as pd
import numpy as np

### Solvency Ratios

def debtToEquity(ticker, timeFrame):
    years = list(data.getLongTermDebt(ticker, timeFrame).keys())
    debt = list(data.getLongTermDebt(ticker, timeFrame).values())
    equity = list(data.getShareholderEquity(ticker, timeFrame).values())
    debt_equity = np.divide(equity, debt)
    d_e = [round(de, 2) for de in debt_equity]
    return {years[i]: d_e[i] for i in range(len(d_e))}

def debtToAssets(ticker, timeFrame):
    years = list(data.getLongTermDebt(ticker, timeFrame).keys())
    debt = list(data.getLongTermDebt(ticker, timeFrame).values())
    assets = list(data.getTotalAssets(ticker, timeFrame).values())
    d_a = np.divide(debt, assets)
    debt_assets = [round(de, 2) for de in d_a]
    return {years[i]: debt_assets[i] for i in range(len(debt_assets))}

def equityToAssets(ticker, timeFrame):
    years = list(data.getShareholderEquity(ticker, timeFrame).keys())
    equity = list(data.getShareholderEquity(ticker, timeFrame).values())
    assets = list(data.getTotalAssets(ticker, timeFrame).values())
    e_a = np.divide(equity, assets)
    equity_assets = [round(ea, 2) for ea in e_a]
    return {years[i]: equity_assets[i] for i in range(len(equity_assets))}

def interestCoverage(ticker):
    interest = list(data.getInterest(ticker).values())[1:]
    years = list(data.getEBITDA(ticker, "A").keys())[0:len(interest)]
    ebitda = list(data.getEBITDA(ticker, "A").values())[0:len(interest)]
    ic = np.divide(ebitda, interest)
    interest_cov = [round(i, 2) for i in ic]
    return {years[i]: interest_cov[i] for i in range(len(interest_cov))}

def assetToLiab(stock, timeFrame):
    total_assets = list(data.getTotalAssets(stock, timeFrame).values())
    total_liab = list(data.getTotalLiab(stock, timeFrame).values())
    asset_liab = [round(total_assets[i] / total_liab[i], 2) for i in range(len(total_assets))]
    years = list(data.getTotalAssets(stock, timeFrame).keys())
    final = dict(zip(years, asset_liab))
    return final

# Profitability

def grossMargin(ticker, timeFrame):
    years = list(data.getRevenue(ticker, timeFrame).keys())
    grossProfit = list(data.getGrossProfit(ticker, timeFrame).values())
    revenue = list(data.getRevenue(ticker, timeFrame).values())
    margin = np.divide(grossProfit, revenue)
    g_margin = [round(m * 100, 2) for m in margin]
    return {years[i]: g_margin[i] for i in range(len(g_margin))}

def operatingMargin(ticker, timeFrame):
    years = list(data.getRevenue(ticker, timeFrame).keys())
    operatingProfit = list(data.getOperatingIncome(ticker, timeFrame).values())
    revenue = list(data.getRevenue(ticker, timeFrame).values())
    margin = np.divide(operatingProfit, revenue)
    o_margin = [round(m * 100, 2) for m in margin]
    return {years[i]: o_margin[i] for i in range(len(o_margin))}

def ebitMargin(ticker, timeFrame):
    years = list(data.getRevenue(ticker, timeFrame).keys())
    ebit = list(data.getEbit(ticker, timeFrame).values())
    revenue = list(data.getRevenue(ticker, timeFrame).values())
    margin = np.divide(ebit, revenue)
    e_margin = [round(m * 100, 2) for m in margin]
    return {years[i]: e_margin[i] for i in range(len(e_margin))}

def ebitdaMargin(ticker, timeFrame):
    years = list(data.getRevenue(ticker, timeFrame).keys())
    ebitda = list(data.getEBITDA(ticker, timeFrame).values())
    revenue = list(data.getRevenue(ticker, timeFrame).values())
    margin = np.divide(ebitda, revenue)
    e_margin = [round(m * 100, 2) for m in margin]
    return {years[i]: e_margin[i] for i in range(len(e_margin))}

def netMargin(ticker, timeFrame):
    years = list(data.getRevenue(ticker, timeFrame).keys())
    netProfit = list(data.getNetIncome(ticker, timeFrame).values())
    revenue = list(data.getRevenue(ticker, timeFrame).values())
    margin = np.divide(netProfit, revenue)
    n_margin = [round(m * 100, 2) for m in margin]
    return {years[i]: n_margin[i] for i in range(len(n_margin))}

def revenueGrowth(ticker, timeFrame):
    revenue = list(data.getRevenue(ticker, timeFrame).values())
    years = list(data.getRevenue(ticker, timeFrame).keys())
    rev = pd.Series(revenue)
    rev=  rev.iloc[::-1]
    rev = rev.pct_change()
    rev=  rev.iloc[::-1]
    rev = [round(x, 4) for x in rev if np.isnan(x) == False]
    return {years[i]: rev[i] for i in range(len(rev))}

def netIncomeGrowth(ticker, timeFrame):
    netProfit = list(data.getNetIncome(ticker, timeFrame).values())
    years = list(data.getNetIncome(ticker, timeFrame).keys())
    net = pd.Series(netProfit)
    net=  net.iloc[::-1]
    net = net.pct_change()
    net=  net.iloc[::-1]
    net = [round(x, 4) for x in net if np.isnan(x) == False]
    return {years[i]: net[i] for i in range(len(net))}

def epsGrowth(ticker, timeFrame):
    eps = list(data.getEPS(ticker, timeFrame).values())
    years = list(data.getEPS(ticker, timeFrame).keys())
    eps = pd.Series(eps)
    eps=  eps.iloc[::-1]
    eps = eps.pct_change()
    eps=  eps.iloc[::-1]
    eps = [round(x, 4) for x in eps if np.isnan(x) == False]
    return {years[i]: eps[i] for i in range(len(eps))}

def roe(ticker, timeFrame):
    years = list(data.getShareholderEquity(ticker, timeFrame).keys())
    netIncome = list(data.getNetIncome(ticker, timeFrame).values())
    equity = list(data.getShareholderEquity(ticker, timeFrame).values()) 
    roe = np.divide(netIncome, equity)
    roe = [round(r, 4) for r in roe]
    return {years[i]: roe[i] for i in range(len(equity))}

def roa(ticker, timeFrame):
    years = list(data.getTotalAssets(ticker, timeFrame).keys())
    netIncome = list(data.getNetIncome(ticker, timeFrame).values())
    equity = list(data.getTotalAssets(ticker, timeFrame).values()) 
    roa = np.divide(netIncome, equity)
    roa = [round(r, 4) for r in roa]
    return {years[i]: roa[i] for i in range(len(equity))}

## Liquidity ratios

def currentRatio(ticker, timeFrame):
    currentAssets = list(data.getCurrentAssets(ticker, timeFrame).values())
    currentLiab = list(data.getCurrentLiab(ticker, timeFrame).values())
    years = list(data.getCurrentAssets(ticker, timeFrame).keys())
    cr= np.divide(currentAssets, currentLiab)
    cr =  [round(c, 2) for c in cr]
    return {years[i]: cr[i] for i in range(len(currentAssets))}

def quickRatio(ticker, timeFrame):
    currentAssets = list(data.getCurrentAssets(ticker, timeFrame).values())
    currentLiab = list(data.getCurrentLiab(ticker, timeFrame).values())
    inventory = list(data.getInventory(ticker, timeFrame).values())
    years = list(data.getCurrentAssets(ticker, timeFrame).keys())
    currAssets = [currentAssets[c] - inventory[c] for c in range(len(currentAssets))]
    cr= np.divide(currAssets, currentLiab)
    cr =  [round(c, 2) for c in cr]
    return {years[i]: cr[i] for i in range(len(currentAssets))}


def daysSalesOutstanding(ticker):
    recievables = list(data.getRecievables(ticker, "A").values())
    revenue = list(data.getRevenue(ticker, "A").values())
    years = list(data.getRevenue(ticker, "A").keys())
    rev = [r / 365 for r in revenue]
    sales = np.divide(recievables , rev)
    return {years[i]: round(sales[i], 2) for i in range(len(years))}

def operatingCashFlowRatio(ticker):
    operatingCF = list(data.getOperatingCF(ticker).values())
    years = list(data.getOperatingCF(ticker).keys())
    currentLiab = list(data.getCurrentLiab(ticker, "A").values())
    ocf = np.divide(operatingCF, currentLiab)
    return {years[i]: round(ocf[i], 2) for i in range(len(years))}


## Effinciency ratios

def operatingExpRatio(ticker):
    cogs = list(data.getCOGS(ticker, 'A').values())
    years = list(data.getCOGS(ticker, 'A').keys())
    operatingExp = list(data.getOperatingExpenses(ticker, 'A').values())
    revenue = list(data.getRevenue(ticker, 'A').values())
    exp = [cogs[e] + operatingExp[e] for e in range(len(operatingExp))]
    opRatio = np.divide(exp, revenue)
    return {years[i]: round(opRatio[i], 2) for i in range(len(years))}

def inventoryTurnover(ticker):
    inventory = list(data.getInventory(ticker, 'A').values())
    cogs = list(data.getCOGS(ticker, 'A').values())
    years = list(data.getCOGS(ticker, 'A').keys())
    inv = [inventory[i + 1] + inventory[i] for i in range(len(inventory)-1)]
    avgInv = [inv[i] / 2 for i in range(len(inv))]
    turnover = [cogs[i] / avgInv[i] for i in range(len(avgInv))]
    return {years[i]: round(turnover[i], 2) for i in range(len(turnover))}

def recievableTurnover(ticker):
    receievable = list(data.getRecievables(ticker, 'A').values())
    rev = list(data.getRevenue(ticker, 'A').values())
    years = list(data.getRevenue(ticker, 'A').keys())
    rec = [receievable[i + 1] + receievable[i] for i in range(len(receievable)-1)]
    avgRec = [rec[i] / 2 for i in range(len(rec))]
    turnover = [rev[i] / avgRec[i] for i in range(len(avgRec))]
    return {years[i]: round(turnover[i], 2) for i in range(len(turnover))}

def payableTurnover(ticker):
    payable = list(data.getPayables(ticker).values())
    cogs = list(data.getCOGS(ticker, 'A').values())
    years = list(data.getCOGS(ticker, 'A').keys())
    rec = [payable[i + 1] + payable[i] for i in range(len(payable)-1)]
    avg = [rec[i] / 2 for i in range(len(rec))]
    turnover = [cogs[i] / avg[i] for i in range(len(avg))]
    return {years[i]: round(turnover[i], 2) for i in range(len(turnover))}

def assetTurnover(ticker):
    asset = list(data.getTotalAssets(ticker, 'A').values())
    rev = list(data.getRevenue(ticker, 'A').values())
    years = list(data.getRevenue(ticker, 'A').keys())
    rec = [asset[i + 1] + asset[i] for i in range(len(asset)-1)]
    avg = [rec[i] / 2 for i in range(len(rec))]
    turnover = [rev[i] / avg[i] for i in range(len(avg))]
    return {years[i]: round(turnover[i], 2) for i in range(len(turnover))}

def workingCapTurnover(ticker):
    cur_assets = list(data.getCurrentAssets(ticker, 'A').values())
    cur_liab = list(data.getCurrentLiab(ticker, 'A').values())
    wc = [cur_assets[i] - cur_liab[i] for i in range(len(cur_assets))]
    rev = list(data.getRevenue(ticker, 'A').values())
    years = list(data.getRevenue(ticker, 'A').keys())
    rec = [wc[i + 1] + wc[i] for i in range(len(wc)-1)]
    avg = [rec[i] / 2 for i in range(len(rec))]
    turnover = [rev[i] / avg[i] for i in range(len(avg))]
    return {years[i]: round(turnover[i], 2) for i in range(len(turnover))}

# Valuations

def bookValue(ticker, timeFrame):
    total_assets = list(data.getTotalAssets(ticker, timeFrame).values())
    total_liab = list(data.getTotalLiab(ticker, timeFrame).values())
    years = list(data.getTotalAssets(ticker, timeFrame).keys())
    book = [total_assets[i] - total_liab[i] for i in range(len(total_assets))]
    return dict(zip(years, book))

def bookPerShare(ticker, timeFrame):
    years = list(data.getSharesOutstanding(ticker, timeFrame).keys())
    shares = list(data.getSharesOutstanding(ticker, timeFrame).values())
    book = list(bookValue(ticker, timeFrame).values())
    perShare = [round(book[i] / shares[i], 2) for i in range(len(book))]
    return dict(zip(years, perShare))

def pe(ticker):
    eps = list(data.getEPS(ticker, 'Q').values())[0:5]
    price = data.price(ticker)
    ttm = np.sum(eps)
    return round(price / ttm, 2)

def priceToBook(ticker):
   book = list(bookPerShare(ticker, "Q").values())[0]
   price = data.price(ticker)
   return round(price / book, 2)

def priceToSales(ticker):
    rev = list(data.getRevenue(ticker, 'Q').values())[0:5]
    ttm = np.sum(rev)
    shares = list(data.getSharesOutstanding(ticker, "Q").values())[0]
    revPerShare = round(ttm / shares, 2)
    price = data.price(ticker)
    return round(price / revPerShare, 2)

def fcfPerShare(ticker):
    fcf = list(data.fcf(ticker).values())
    years = list(data.fcf(ticker).keys())
    shares = list(data.getSharesOutstanding(ticker, "A").values())
    perShare = [round(fcf[i] / shares[i], 2) for i in range(len(fcf))]
    return dict(zip(years, perShare))

def priceToFCF(ticker):
    price = data.price(ticker)
    fcf = list(fcfPerShare(ticker).values())[0]
    return round(price / fcf, 2)

def divYield(ticker):
    price = data.price(ticker)
    div = data.ttmDivs(ticker)
    return round(div / price, 4)
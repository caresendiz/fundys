import yfinance as yf

def sp500(timeFrame):
    return yf.Ticker('^GSPC').history(timeFrame)['Close']

def vix(timeFrame):
    return yf.Ticker('^VIX').history(timeFrame)['Close']

def dow(timeFrame):
    return yf.Ticker('^DJI').history(timeFrame)['Close']

def nasComposite(timeFrame):
    return yf.Ticker('^IXIC').history(timeFrame)['Close']

def russel2000(timeFrame):
    return yf.Ticker('^RUT').history(timeFrame)['Close']

def treasury(timeFrame):
    return yf.Ticker('^TNX').history(timeFrame)['Close']

def tbill13(timeFrame):
    return yf.Ticker('^IRX').history(timeFrame)['Close']

def nas100(timeFrame):
    return yf.Ticker('^NDX').history(timeFrame)['Close']

def nikkei(timeFrame):
    return yf.Ticker('^N225').history(timeFrame)['Close']

def ipcMex(timeFrame):
    return yf.Ticker('^MXX').history(timeFrame)['Close']

def crudeVol(timeFrame):
    return yf.Ticker('^OVX').history(timeFrame)['Close']

def nas100premarket(timeFrame):
    return yf.Ticker('^QMI').history(timeFrame)['Close']

def nas100afterHours(timeFrame):
    return yf.Ticker('^QIV').history(timeFrame)['Close']

def russel1000(timeFrame):
    return yf.Ticker('^RUI').history(timeFrame)['Close']

def russel3000(timeFrame):
    return yf.Ticker('^RUA').history(timeFrame)['Close']

def treasury30(timeFrame):
    return yf.Ticker('^TYX').history(timeFrame)['Close']

def nadVol(timeFrame):
    return yf.Ticker('^VXN').history(timeFrame)['Close']

def spVol3M(timeFrame):
    return yf.Ticker('^VIX3M').history(timeFrame)['Close']
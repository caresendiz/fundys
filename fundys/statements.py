import pandas as pd
from bs4 import BeautifulSoup
import requests

#dependencies

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }

def divide(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def listUp(theList, index, whichList):
    for i in theList:
        whichList.append(i[index])

def removeExtraIndex(indexxx):
  for i in indexxx:
        i.remove('')

def removeDupIndex(indexx, indexxx):
    for i in indexx:
        k = list(dict.fromkeys(i))
        indexxx.append(k)

def joinIndex(indexxx, newIndex):
    for i in range(len(indexxx)):
        k = ' '.join(indexxx[i])
        newIndex.append(k)

def incomeStmt(ticker):
    url = "https://www.marketwatch.com/investing/stock/" + ticker + "/financials"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    priceHtml = soup.find_all("td", class_="overflow__cell")
    yearHtml = soup.find_all("th", class_="overflow__heading")
    years = [s.get_text() for s in yearHtml]
    years = years[1:6]
    table = [i.get_text() for i in priceHtml]
    table = [s.replace('\n', ' ') for s in table]
    table = [s.replace('B', '') for s in table]
    table = [s.replace('%', '') for s in table]
    table = [s.replace('(', '-') for s in table]
    table = [s.replace(')', '') for s in table]
    x = list(divide(table, 7))
    index = []
    year1 = []
    year2 = []
    year3 = []
    year4 = []
    year5 = []
    listUp(x, 0, index)
    listUp(x, 1, year1)
    listUp(x, 2, year2)
    listUp(x, 3, year3)
    listUp(x, 4, year4)
    listUp(x, 5, year5)
    index = [s.replace('\n', ' ') for s in index]
    index = [s.split(' ') for s in index]
    indexx= []
    removeDupIndex(index, indexx)
    removeExtraIndex(indexx) 
    newIndex = []
    joinIndex(indexx, newIndex)
    year1 = [s.replace('M', '') for s in year1]
    year2 = [s.replace('M', '') for s in year2]
    year3 = [s.replace('M', '') for s in year3]
    year4 = [s.replace('M', '') for s in year4]
    year5 = [s.replace('M', '') for s in year5]
    financialStmt = pd.DataFrame()
    financialStmt['Category']=newIndex
    financialStmt[years[0]]=year1
    financialStmt[years[1]]=year2
    financialStmt[years[2]]=year3
    financialStmt[years[3]]=year4
    financialStmt[years[4]]=year5
    financialStmt = financialStmt.set_index('Category')
    return financialStmt

def balanceSheet(ticker):
    url = "https://www.marketwatch.com/investing/stock/" + ticker + "/financials/balance-sheet"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    priceHtml = soup.find_all("td", class_="overflow__cell")
    yearHtml = soup.find_all("th", class_="overflow__heading")
    years = [s.get_text() for s in yearHtml]
    years = years[1:6]
    table = [i.get_text() for i in priceHtml]
    table = [s.replace('\n', ' ') for s in table]
    table = [s.replace('B', '') for s in table]
    table = [s.replace('%', '') for s in table]
    table = [s.replace('(', '-') for s in table]
    table = [s.replace(')', '') for s in table]
    x = list(divide(table, 7))
    index = []
    year1 = []
    year2 = []
    year3 = []
    year4 = []
    year5 = []
    listUp(x, 0, index)
    listUp(x, 1, year1)
    listUp(x, 2, year2)
    listUp(x, 3, year3)
    listUp(x, 4, year4)
    listUp(x, 5, year5)
    index = [s.replace('\n', ' ') for s in index]
    index = [s.split(' ') for s in index]
    indexx= []
    removeDupIndex(index, indexx)
    removeExtraIndex(indexx) 
    newIndex = []
    joinIndex(indexx, newIndex)
    year1 = [s.replace('M', '') for s in year1]
    year2 = [s.replace('M', '') for s in year2]
    year3 = [s.replace('M', '') for s in year3]
    year4 = [s.replace('M', '') for s in year4]
    year5 = [s.replace('M', '') for s in year5]
    financialStmt = pd.DataFrame()
    financialStmt['Category']=newIndex
    financialStmt[years[0]]=year1
    financialStmt[years[1]]=year2
    financialStmt[years[2]]=year3
    financialStmt[years[3]]=year4
    financialStmt[years[4]]=year5
    financialStmt = financialStmt.set_index('Category')
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    return financialStmt

def cashFlow(ticker):
    url = "https://www.marketwatch.com/investing/stock/" + ticker + "/financials/cash-flow"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    priceHtml = soup.find_all("td", class_="overflow__cell")
    yearHtml = soup.find_all("th", class_="overflow__heading")
    years = [s.get_text() for s in yearHtml]
    years = years[1:6]
    table = [i.get_text() for i in priceHtml]
    table = [s.replace('\n', ' ') for s in table]
    table = [s.replace('B', '') for s in table]
    table = [s.replace('%', '') for s in table]
    table = [s.replace('(', '-') for s in table]
    table = [s.replace(')', '') for s in table]
    x = list(divide(table, 7))
    index = []
    year1 = []
    year2 = []
    year3 = []
    year4 = []
    year5 = []
    listUp(x, 0, index)
    listUp(x, 1, year1)
    listUp(x, 2, year2)
    listUp(x, 3, year3)
    listUp(x, 4, year4)
    listUp(x, 5, year5)
    index = [s.replace('\n', ' ') for s in index]
    index = [s.split(' ') for s in index]
    indexx= []
    removeDupIndex(index, indexx)
    removeExtraIndex(indexx) 
    newIndex = []
    joinIndex(indexx, newIndex)
    year1 = [s.replace('M', '') for s in year1]
    year2 = [s.replace('M', '') for s in year2]
    year3 = [s.replace('M', '') for s in year3]
    year4 = [s.replace('M', '') for s in year4]
    year5 = [s.replace('M', '') for s in year5]
    financialStmt = pd.DataFrame()
    financialStmt['Category']=newIndex
    financialStmt[years[0]]=year1
    financialStmt[years[1]]=year2
    financialStmt[years[2]]=year3
    financialStmt[years[3]]=year4
    financialStmt[years[4]]=year5
    financialStmt = financialStmt.set_index('Category')
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    return financialStmt

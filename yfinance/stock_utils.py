import csv
from dataclasses import asdict, dataclass
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as soup
import pandas as pd


@dataclass
class StockData:
    data_symbol: str # Stock ticker. "BRK-A"
    data_field: str # Statistics field name. "targetMeanPrice"
    data_value: str # Statistics field value. "715,333.00"

"""
Returns stock data for a given ticker symbol
"""
def fetchStock(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/'

    try:
        # Loading Page
        response = requests.get(url)
        print(response.text)
        yFinancePage = soup(response.text, 'lxml')

        # Making Stock object
        stock_data = _getStockData(yFinancePage)
        return stock_data

    except ConnectionError:
        return None


"""
Helper method that builds a StockData parsed from Yahoo Finance.  
"""
def _getStockData(yFinancePage):
    # List of data fields to parse out of yFinancePage
    data_fields = [
        "regularMarketPrice", "regularMarketChange", "regularMarketChangePercent",
        "regularMarketPreviousClose", "regularMarketOpen", "regularMarketDayRange",
        "fiftyTwoWeekRange", "regularMarketVolume", "averageVolume", "marketCap", "targetMeanPrice"]

    # Building list of StockData objects for a given ticker.
    stock_data = []

    for data_field in data_fields:
        data = yFinancePage.find('fin-streamer', {'data-field': data_field})

        # Building stock data object
        sd = StockData(data_symbol=data['data-symbol'],
                       data_field=data['data-field'],
                       data_value=data['data-value'])

        # Storing the value on the returning list
        stock_data.append(sd)

    return stock_data






"""
Writes stock data to given outputs
"""
def out(stocks, csv, json, console):

    if console:
        print(stocks)

    # Writing to CSV
    if csv != None:
        df = pd.json_normalize(asdict(data) for data in stocks)
        df.to_csv(csv, sep='\t', encoding='utf-8', index=False, header=True)

    if json != None:
        # Hard coding the json format with a dictionary
        _stocks = {}
        for stock in stocks:
            # Making new entry if one doesn't exist already
            if not _stocks.__contains__(stock.data_symbol):
                _stocks[stock.data_symbol] = []

            # Json entry
            data = {
                stock.data_field : stock.data_value
            }

            _stocks[stock.data_symbol].append(data)

        df = pd.DataFrame.from_dict(_stocks)
        df.to_json(json, index=False)



import pandas as pd
import robin_stocks as r
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class Stock():
    def __init__(self, ticker):
        self.ticker = ticker
        


    def get_historicals(self,interval='day', span='year'):
        # Returns Pandas Data Frame with stock volume, close, open, high,low, and normed return values.  
        hist = r.stocks.get_stock_historicals('{}'.format(self.ticker), interval ='day', span='year', bounds='regular', info=None)
        self.hist = pd.DataFrame(hist)
        self.hist['begins_at']=pd.to_datetime(self.hist['begins_at'])
        self.hist.set_index('begins_at',inplace=True)
        self.hist['close_price'] = pd.to_numeric(self.hist['close_price'])
        self.hist['open_price'] = pd.to_numeric(self.hist['open_price'])
        self.hist['high_price'] = pd.to_numeric(self.hist['high_price'])
        self.hist['low_price'] = pd.to_numeric(self.hist['low_price'])
        self.hist['normed_return'] =self.hist['close_price']/self.hist.iloc[0]['close_price']
        self.hist.drop('session', axis = 1, inplace=True)
        self.hist.drop('interpolated', axis = 1, inplace=True)
        self.hist.drop('symbol', axis = 1, inplace=True)
        self.hist['20_day_mean'] = self.hist['close_price'].rolling(20).mean()
        self.hist['upper'] = self.hist['20_day_mean']+2*(self.hist['close_price'].rolling(20).std())
        self.hist['lower'] = self.hist['20_day_mean']-2*(self.hist['close_price'].rolling(20).std())
        return self.hist
    
    def get_daily(self):
        # Returns Pandas Data Frame with stock volume, close, open, high,low, and normed return values.  
        daily = r.stocks.get_stock_historicals('{}'.format(self.ticker), interval ='5minute', span='day', bounds='regular', info=None)
        self.daily = pd.DataFrame(daily)
        self.daily['begins_at']=pd.to_datetime(self.daily['begins_at'])
        self.daily.set_index('begins_at',inplace=True)
        self.daily['close_price'] = pd.to_numeric(self.daily['close_price'])
        self.daily['open_price'] = pd.to_numeric(self.daily['open_price'])
        self.daily['high_price'] = pd.to_numeric(self.daily['high_price'])
        self.daily['low_price'] = pd.to_numeric(self.daily['low_price'])
        self.daily['normed_return'] =self.daily['close_price']/self.daily.iloc[0]['close_price']
        self.daily.drop('session', axis = 1, inplace=True)
        self.daily.drop('interpolated', axis = 1, inplace=True)
        self.daily.drop('symbol', axis = 1, inplace=True)
        self.daily['30_min_mean'] = self.daily['close_price'].rolling(6).mean()
        self.daily['upper'] = self.daily['30_min_mean']+2*(self.daily['close_price'].rolling(6).std())
        self.daily['lower'] = self.daily['30_min_mean']-2*(self.daily['close_price'].rolling(6).std())
        return self.daily

    def get_price(self):
        # returns price as a string
        quote = r.stocks.get_quotes(self.ticker)
        self.quote = pd.DataFrame(quote)
        self.quote = self.quote.iloc[0][4]
        self.quote = self.quote[0:-4]
        return self.quote
    
    def get_info(self):
        self.info = r.stocks.get_fundamentals(self.ticker)
        # self.description = self.info[0]['description']
        # self.high_52 = float(info[0]['high_52_weeks'])
        # self.low_52 = float(info[0]['low_52_weeks'])
        # self.daily_high = float(info[0]['high'])
        # self.daily_low = float(info[0]['low'])
        # self.open_price= float(info[0]['open'])

    def view_options(self):
    #Set Browser path and options
        PATH = "/Users/jfonz/Documents/Webdriver/chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        wd = webdriver.Chrome(PATH, options=options)  
    # Site parameters
        ticker = arkk.ticker.upper()
        site = 'https://finance.yahoo.com/quote/{}/options?p={}'.format(ticker,ticker)
        wd.get(site)
        html = wd.page_source
        df = pd.read_html(html)
        print(df[0])

if __name__ == "__main__":  
    arkk = Stock('pltr')    
    arkk.view_options()

    # get options chain dates
    # load tables for date
    # find optimal spreads
    # find optimal returns
    # calender spreads
    # strangles (high volitility)
    # iron condors (low volility)
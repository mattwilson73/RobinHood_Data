import datetime as dt
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import pandas as pd
from matplotlib import style
import matplotlib as mpl
import numpy as np

class Stock2:
    def __init__(self, ticker, years = 5):
        self.ticker = ticker
        self.pricehistory = None
        self.data = None
        self.source = 'yahoo'
        self.start = dt.datetime.now() - dt.timedelta(days=(365*years))
        self.end = dt.date.today()

        self.shares = 0

        self.grab_data()


    def grab_data(self):
        '''Produces a DataFrame of stock data'''
        self.data = web.DataReader(self.ticker, self.source, self.start, self.end)


    def buy(self, quantity):
        self.shares += quantity

    def sell(self, quantity):
        self.shares -= quantity

    """Getters"""
    def get_ticker(self):
        return str(self.ticker)

    def get_shares(self):
        return self.shares

    def get_price_data(self):
        '''Returns a Series of just closing prices'''
        return self.data['Adj Close'].rename(self.ticker)

    def get_current_price(self):
        return float(self.get_price_data().tail(1))



class Transaction:
    def __init__(self,t):
        self.ticker = t[0]
        self.name = t[1]
        self.date = t[2]
        self.quantity = t[3]
        self.price = t[4]
        self.trantype = t[5]
        self.fee = t[6]
        self.total = t[7]

    def get_ticker(self):
        return str(self.ticker)

    def get_name(self):
        return str(self.name)

    def get_date(self):
        return self.date

    def get_quantity(self):
        return float(self.quantity)

    def get_price(self):
        return float(self.price)

    def get_trantype(self):
        return str(self.trantype)

    def get_fee(self):
        return float(self.fee)

    def get_total(self):
        return float(self.total)








class Port:
    def __init__(self, tlist):
        self.tlist = tlist
        self.portfolio = {}

        self.gen_portfolio()

    def gen_portfolio(self):
        for t in self.tlist:

            if t.get_ticker() not in self.portfolio:
                self.portfolio[t.get_ticker()] = Stock2(t.get_ticker())


        for t in self.tlist:
            if t.get_trantype() == 'buy':
                self.portfolio[t.get_ticker()].buy(t.get_quantity())

            if t.get_trantype() == 'sell':
                self.portfolio[t.get_ticker()].sell(t.get_quantity())


    def show_holdings(self):
        for x in self.portfolio:
            print(self.portfolio.get(x).get_shares())






def load_transactions():
    transactions_df = pd.read_excel('stockdata.xls', sheet_name='Transactions')
    tlist = []

    for t in transactions_df.values.tolist():
        tlist.append(Transaction(t))

    return tlist



myt = load_transactions()


myport = Port(myt)

myport.show_holdings()





import datetime as dt
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import pandas as pd
from matplotlib import style
import matplotlib as mpl
import numpy as np

#df = pd.read_excel('stockdata.xls',sheet_name='Summary')
#df = df[df['Quantity in hand'] > 0]
#dt.datetime().today() - dt.timedelta(days=5 * 365)



class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.df = None
        self.closedf = None
        self.movavg = None
        self.start = dt.datetime.now() - dt.timedelta(days=1825)
        self.end = dt.date.today()

        self.grabdata()

    def grabdata(self):
        self.df = web.DataReader(self.ticker, 'yahoo', self.start, self.end)
        self.closedf = self.df['Adj Close']
        # self.closedf.rename(columns={'Adj Close':str(self.ticker)},inplace=True)

        self.movavg = self.closedf.rolling(window=1825).mean()

    def getticker(self):
        return self.ticker

    def getdata(self):
        return self.closedf

    def getdpc(self):
        return np.log(1+self.closedf.pct_change())

    def plotdf(self):
        mpl.rc('figure',figsize=(8,7))
        style.use('ggplot')
        self.closedf.plot(label=self.ticker)
        #self.movavg.plot(label='Moving Average')
        plt.legend()
        plt.show()


class Portfolio:
    def __init__(self, holdings = []):
        self.holdings = holdings
        self.portfolio = []
        self.returns = []
        self.dpc = None
        self.genPortfolio()
        self.genDPC()

    def genPortfolio(self):
        for t in self.holdings:
            self.portfolio.append(Stock(t))

    def genDPC(self):
        dpcdata = []

        for s in self.portfolio:
            dpcdata.append(s.getdpc())

        self.dpc = pd.concat(dpcdata, axis='columns' ,join='inner')

    def genReturns(self):
        # for s in self.portfolio:
        #     self.returns =
        pass


    def plotDPC(self):
        self.dpc.plot(figsize=(20,10), title='Daily Returns')
        plt.legend(self.holdings)
        plt.show()



testHoldings = ['AAPL','AMZN','FB','GE']

myport = Portfolio(testHoldings)

myport.plotDPC()



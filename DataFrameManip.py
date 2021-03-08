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
        self.dpc = None
        self.start = dt.datetime.now() - dt.timedelta(days=1825)
        self.end = dt.date.today()

        self.grab_data()

    def grab_data(self):
        self.df = web.DataReader(self.ticker, 'yahoo', self.start, self.end)
        self.closedf = self.df['Adj Close']
        # self.closedf.rename(columns={'Adj Close':str(self.ticker)},inplace=True)

        self.movavg = self.closedf.rolling(window=1825).mean()

    def getticker(self):
        return self.ticker

    def getdata(self):
        return self.closedf

    def gendpc(self):
        self.dpc = np.log(1+self.closedf.pct_change())

    def getdpc(self):
        return self.dpc

    def genCumulRet(self):
        pass

    def plotdf(self):
        mpl.rc('figure',figsize=(8,7))
        style.use('ggplot')
        self.closedf.plot(label=self.ticker)
        #self.movavg.plot(label='Moving Average')
        plt.legend()
        plt.show()


class Portfolio:
    def __init__(self, holdings = None):
        self.holdings = holdings
        self.portfolio = []
        self.returns = []
        self.weights = []
        self.dpc = None
        self.genPortfolio()
        self.genDPC()

    def genPortfolio(self):
        for t in self.holdings['Ticker'].tolist():
            self.portfolio.append(Stock(t))

    def genDPC(self):
        dpcdata = []

        for s in self.portfolio:
            dpcdata.append(s.getdpc())

        self.dpc = pd.concat(dpcdata, axis='columns' ,join='inner')

        print(self.dpc)

    def genReturns(self):
        pass


    def getHoldings(self):
        '''Returns a list of holdings'''
        return self.holdings['Ticker'].tolist()

    def plotDPC(self):
        self.dpc.plot(figsize=(15,10), title='Daily Returns')
        plt.legend(self.holdings['Ticker'].tolist())
        plt.show()





def holdingsimporter():
    df = pd.read_excel('stockdata.xls', sheet_name='Summary',usecols="A,G")
    df = df[df['Quantity in hand'] > 0]



    return df


myholdings = holdingsimporter()

myport = Portfolio(myholdings)

print(type(myport[0].getdpc()))


# myport.plotDPC()
#
# testHoldings = ['AAPL','AMZN','FB','GE']

# testport = Portfolio(testHoldings)
# testport.plotDPC()


# print(x['Ticker'].tolist())
# print(x['Quantity in hand'].to_list())
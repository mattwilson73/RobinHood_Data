import pandas_datareader as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tslaQuote = web.DataReader('TSLA',data_source='yahoo',start='2010-01-01',end='2018-12-31')

stocks = ['GOOGL', 'TM', 'KO', 'PEP']
numAssets = len(stocks)
source = 'yahoo'
start = '2010-01-01'
end = ' 2019-5-31'

data = pd.DataFrame(columns=stocks)
for symbol in stocks:
  data[symbol] = web.DataReader(symbol, data_source=source, start=start, end=end)['Adj Close']

percent_change = data.pct_change()
returns = np.log(1+percent_change)
returns.head()

meanDailyReturns = returns.mean()
covMatrix = returns.cov()

weights = np.array([0.5,0.2,0.2,0.1])
portReturn = np.sum(meanDailyReturns*weights)
portStdDev = np.sqrt(np.dot(weights.T,np.dot(covMatrix,weights)))

plt.figure(figsize=(14, 7))
for c in returns.columns.values:
  plt.plot(returns.index, returns[c], lw=3, alpha=0.8, label=c)

plt.legend(loc='upper left', fontsize=12)
plt.ylabel('returns')

plt.show()

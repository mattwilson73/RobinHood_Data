import datetime as dt
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import pandas as pd





df = pd.read_excel('stockdata.xls',sheet_name='Summary')
print(df)
holdings = df[df['Quantity in hand'] > 0]

#print(df['Ticker'])
tickers = []

for t in holdings["Ticker"]:
    tickers.append(t)

amounts = []
for qnty in holdings['Quantity in hand']:
    amounts.append(qnty)
prices =[]
total=[]

for ticker in tickers:
    df = web.DataReader(ticker, 'yahoo', dt.datetime(2019,8,1), dt.datetime.now())
    price = df[-1:]['Close'][0]
    prices.append(price)
    index = prices.index(price)
    total.append(price * amounts[index])


def piechart(tickers,amounts,prices,total):
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    now = dt.datetime.now()
    date_time = now.strftime("%m/%d/%Y")
    ax.set_title("PortViz as of "+date_time, color='#EF6C35', fontsize=20)

    patches, texts, autotexts = ax.pie(total, labels=tickers, autopct='%1.1f%%', pctdistance=0.8)
    [text.set_color('white') for text in texts]

    my_circle = plt.Circle((0, 0), 0.55, color='black')
    plt.gca().add_artist(my_circle)

    ax.text(-2, 1, 'PORTFOLIO OVERVIEW:', fontsize=14, color="#ffe536", horizontalalignment='center',
            verticalalignment='center')

    ax.text(-2, 0.85, f'Total USD Amount: {sum(total):.2f} $', fontsize=12, color="white", horizontalalignment='center',
            verticalalignment='center')
    counter = 0.15
    for ticker in tickers:
        ax.text(-2, 0.85 - counter, f'{ticker}: {total[tickers.index(ticker)]:.2f} $', fontsize=12, color="white",
                horizontalalignment='center', verticalalignment='center')
        counter += 0.15

    plt.show()


piechart(tickers,amounts,prices,total)
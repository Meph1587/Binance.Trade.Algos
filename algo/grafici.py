from binance.client import Client
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

client= Client("", "")

coin= client.get_historical_klines(symbol='ETHBTC', interval= '1d', start_str= '2018.01.01', end_str= '2018.08.21')
coin_tb= pd.DataFrame(coin, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

coin_tb['Open time']= pd.to_datetime(coin_tb['Open time'], unit='ms')
time= coin_tb['Open time']

coin_tb['Close'] = coin_tb['Close'].astype(float)
plt.plot(time,coin_tb['Close'],'g',label= 'Current price')

coin_tb['High']= coin_tb['High'].astype(float)
coin_tb['Low']= coin_tb['Low'].astype(float)
midPrice= (coin_tb['High'] + coin_tb['Low'])/2
plt.plot(time,midPrice,'r',label= 'Mid-price')


coin_tb['MA_9']= coin_tb['Close'].rolling(9).mean()
plt.plot(time,coin_tb['MA_9'],'c',label= '9-day moving average')

coin_tb['MA_26']= coin_tb['Close'].rolling(26).mean()
plt.plot(time,coin_tb['MA_26'],'b',label= '26-day moving average')

#coin_tb['Span A']= (coin_tb['MA_9']+coin_tb['MA_26'])/2

#coin_tb['Span B']=

plt.legend()
plt.grid(True)
plt.show()





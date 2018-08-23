from binance.client import Client
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

client= Client("", "")

coin= client.get_historical_klines(symbol='ETHBTC', interval= '4h', start_str= '2018.01.01', end_str= '2018.08.21')
coin_tb= pd.DataFrame(coin, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

coin_tb['Open time']= pd.to_datetime(coin_tb['Open time'], unit='ms')
time= coin_tb['Open time']
time26  = coin_tb['Open time'] + pd.Timedelta(days=26)

coin_tb['Close'] = coin_tb['Close'].astype(float)
plt.plot(time,coin_tb['Close'],'g',label= 'Current price')

coin_tb['High']= coin_tb['High'].astype(float)
coin_tb['Low']= coin_tb['Low'].astype(float)
midPrice= (coin_tb['High'] + coin_tb['Low'])/2
plt.plot(time,midPrice,'r',label= 'Mid-price')




coin_tb['MA_9']= (coin_tb['Close'].rolling(6).max()+ coin_tb['Close'].rolling(6).min())/2
plt.plot(time,coin_tb['MA_9'],'c',label= '9-period moving average')

coin_tb['MA_26']= (coin_tb['Close'].rolling(26).max()+ coin_tb['Close'].rolling(26).min())/2
plt.plot(time,coin_tb['MA_26'],'b',label= '26-period moving average')

coin_tb['equals'] = np.where(coin_tb['MA_9'] == coin_tb['MA_26'])
plt.plot(time,coin_tb['equals'],'p',label= 'Cross')

coin_tb['Span_A']= (coin_tb['MA_9']+coin_tb['MA_26'])/2
plt.plot(time26,coin_tb['Span_A'],'y',label= 'Span A')

coin_tb['Span_B']= (coin_tb['Close'].rolling(52).max()+ coin_tb['Close'].rolling(52).min())/2
plt.plot(time26,coin_tb['Span_B'],'y',label= 'Span B')

plt.legend()
plt.grid(True)
plt.show()
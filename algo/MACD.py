from binance.client import Client
import datetime
import matplotlib.pyplot as plt
import pandas as pd

client= Client("", "")

def MACD(symbol, interval, start, end, quant, wall):

  coin= client.get_historical_klines(symbol=symbol, interval= interval, start_str= start, end_str= end)
  coin_tb= pd.DataFrame(coin, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

  time= pd.to_datetime(coin_tb['Open time'], unit='ms')
  openPrice= coin_tb['Open'].astype(float)
  plt.plot(time, openPrice, 'b')

  #12-day EMA
  ema1= openPrice.rolling(12).mean()
  #26-day EMA
  ema2= openPrice.rolling(26).mean()

  
  macdLine= ema1-ema2
  #plt.plot(time, macdLine,'r')

  #9-day EMA
  signalLine= macdLine.rolling(9).mean()
  #plt.plot(time, signalLine, 'g')

  macdHistogram= macdLine- signalLine

  buyPhase= True
  sellPhase= False
  quantityBuy= quant
  wallet= wall
  crypto= 0

  highestGain=0
  highestLost=0


  for i in range(len(openPrice)):


    if macdHistogram[i] > 0:
        if buyPhase == True:

            print "BUY, ", "Price:",openPrice[i] , "Time:", time[i], "Quantity:", quantityBuy
            crypto= quantityBuy/openPrice[i]
            wallet-=quantityBuy
            buyPhase= False
            sellPhase= True


    if macdHistogram[i] < 0:
        if sellPhase == True:

            print "SELL, ", "Price:", openPrice[i], "Time:", time[i], "Quantity:", crypto*openPrice[i]
            print " "           
            wallet+= crypto*openPrice[i]                      

            if ((crypto*openPrice[i])- quantityBuy)> 0 and 	((crypto*openPrice[i])- quantityBuy)> highestGain:
                highestGain= (crypto*openPrice[i])- quantityBuy

            if ((crypto*openPrice[i])- quantityBuy)< 0 and 	((crypto*openPrice[i])- quantityBuy)< highestLost:
                highestLost= (crypto*openPrice[i])- quantityBuy

            buyPhase= True
            sellPhase= False  
            crypto=0   

  print " "  
  lenEndTime= len(openPrice)-1
  print "Wallet:", wallet , "Start time:", time[0], "End time:", time[lenEndTime]
  print "Highest Lost:", highestLost
  print "Highest Gain", highestGain
  
  plt.grid(True)
  plt.show()
  
  






#example:
MACD('ETHUSDT','30m','2018.06.01', '2018.08.01',100, 1000)  




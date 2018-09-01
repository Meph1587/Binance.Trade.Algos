from binance.client import Client
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

client= Client("", "")

coin= client.get_historical_klines(symbol='ETHUSDT', interval= '5m', start_str= '2018.08.01', end_str= '2018.08.02')
coin_tb= pd.DataFrame(coin, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

time= pd.to_datetime(coin_tb['Open time'], unit='ms')
closePrice= coin_tb['Close'].astype(float)

def doublingMethod(wall, quant):

  wallet= wall
  quantityBuy= quant
  x= closePrice[0] #first price
  sellPhase= False
  crypto= 0

  #for the plot 
  buyTime= []
  buyPrice= []

  sellTime= [] 
  sellPrice= []


  print "Wallet:", wallet, "Time:", time[0]
  print " "

  for i in range(len(closePrice)):

    if closePrice[i]< 0.99* x or sellPhase== False:   
      crypto+= quantityBuy/closePrice[i] #calculate the value of the money invested
      wallet-= quantityBuy #subtract money invested
      print "BUY, ", "Price:",closePrice[i] , "Time:", time[i], "Quantity:", quantityBuy
      print "Wallet:", wallet
      print "Crypto", crypto
      quantityBuy*= 2 #doublig money invest
      x= closePrice[i]
      sellPhase= True

      buyTime.append(time[i])
      buyPrice.append(closePrice[i])



    if closePrice[i]> 1.01*x and sellPhase== True:

      wallet+= crypto*closePrice[i] #earn money invested
      print " "
      print "SELL, ", "Price:", closePrice[i], "Time:", time[i], "Quantity:", crypto*closePrice[i]
      print "Wallet:", wallet
      print " "
      x= closePrice[i]
      sellPhase= False
      quantityBuy= quant
      crypto= 0

      sellTime.append(time[i])
      sellPrice.append(closePrice[i])

    ++i

  print " "  
  lenEndTime= len(closePrice)-1
  print "Wallet:", wallet , "Start time:", time[0], "End time:", time[lenEndTime]

  plt.plot(time,closePrice,'g',label= 'Price')
  plt.plot(buyTime,buyPrice,'d',label= 'Buy')
  plt.plot(sellTime, sellPrice,'d',label= 'Sell')
  plt.ylabel('PRICE')
  plt.xlabel('TIME')
  plt.legend()
  plt.grid(True)
  plt.show()

  return


#example
doublingMethod(10000, 100)  



























































     









        











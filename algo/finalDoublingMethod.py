from binance.client import Client
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

client= Client("", "")

coin= client.get_historical_klines(symbol='ETHUSDT', interval= '5m', start_str= '2018.07.01', end_str= '2018.08.01')
coin_tb= pd.DataFrame(coin, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

time= pd.to_datetime(coin_tb['Open time'], unit='ms')
closePrice= coin_tb['Close'].astype(float)

def doublingMethod(wall, quant):

 	wallet= wall
 	quantity= quant
 	x= closePrice[0]
 	sellPhase= False
 	quantityBuy= quantity/2
 	investment= 0

	print "Wallet:", wallet, "Time:", time[0]
	print " "

	for i in range(len(closePrice)):

		if closePrice[i]< 0.99* x:
  			quantityBuy*=2
  			investment= (investment* 0.99)+ quantityBuy
  			wallet-= quantityBuy 
  			print "BUY, ", "Price:", x, "Time:", time[0], "Quantity:", quantityBuy
	   		print "Wallet:", wallet
 			x= closePrice[i]
       		sellPhase= True

		if closePrice[i]> 1.01*x and sellPhase== True:
    		wallet+= investment* 1.01
    		print "SELL, ", "Price:", closePrice[i], "Time:", time[i], "Quantity:", investment* 1.01
    		print "Wallet:", wallet
    		print " "
    		x= closePrice[i]
    		sellPhase= False
       		quantityBuy= quantity/2
       		investment= 0

      	++i

    print " "  
    lenEndTime= len(closePrice)-1
    print "Wallet:", wallet, "Start time:", time[0], "End time:", time[lenEndTime]


#example
doublingMethod(10000, 500)  




     









        











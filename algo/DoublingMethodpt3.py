from binance.client import Client
import datetime
import matplotlib.pyplot as plt
import pandas as pd

client= Client("", "")

def doublingMethod(symbol, wal, qBuy):

	#Connection
	coin= client.get_historical_klines(symbol= symbol, interval= '1m', start_str= '2018.09.18 22:00:00', end_str= '2018.09.19 06:00:00')
	coin_tb= pd.DataFrame(coin, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
	time= pd.to_datetime(coin_tb['Open time'], unit='ms')
	closePrice= coin_tb['Close'].astype(float)
	
	wallet= wal 
	quantityBuy= qBuy 

	#Start
	crypto= 0
	x= closePrice[0]	
	sellPhase= False
	stop= 0
	
	#For the plot 
	buyTime= []
	buyPrice= []
	sellTime= [] 
	sellPrice= []


	####
	negativeWallet= 0
	lastWallet= 0
	###

	#Run strategy
	for i in range(len(closePrice)):
		
		

		if (closePrice[i]< 0.992* x or sellPhase== False) and stop< 4:

			#Calculate investment
			crypto+= quantityBuy/closePrice[i] 
			wallet-= quantityBuy
			wallet-= quantityBuy*0.001#TAX

			#'''
			print "BUY|", "Price:", closePrice[i], "Time:", time[i], "Quantity:", quantityBuy
			print "Wallet:", wallet
			print "Crypto", crypto
			print ""
			#'''

			#New condition
			quantityBuy*= 2
			x= closePrice[i]
			sellPhase= True
			stop+= 1

			#Plot
			buyTime.append(time[i])
			buyPrice.append(closePrice[i])


		if closePrice[i]> 1.008*x and sellPhase== True:

			#Calculate gain
			wallet+= closePrice[i]* crypto 
			wallet-= (closePrice[i]* crypto)* 0.001#TAX 

			#'''
			print ""
			print ""	
			print "SELL|", "Price:", closePrice[i], "Time:", time[i], "Quantity:", closePrice[i]* crypto
			print "Wallet:", wallet
			print ""
			print ""
			print ""
			#'''

			#Restore  conditions 
			crypto= 0
			quantityBuy= qBuy
			x= closePrice[i]
			sellPhase= False
			stop= 0

			#plot
			sellTime.append(time[i])
			sellPrice.append(closePrice[i])

			lastWallet= wallet

		if wallet< 0:
		   negativeWallet = time[i]

		   
	#draw plot	   
	plt.plot(time,closePrice,'g',label= 'Price')
	plt.plot(buyTime,buyPrice,'d',label= 'Buy')
	plt.plot(sellTime, sellPrice,'d',label= 'Sell')
	plt.ylabel('PRICE')
	plt.xlabel('TIME')
	plt.legend()
	plt.grid(True)
	
	
	print ""
	print "Guadagno: ", lastWallet-wal

	plt.show()

	return lastWallet


doublingMethod('BNBUSDT', 3600, 200 )

 












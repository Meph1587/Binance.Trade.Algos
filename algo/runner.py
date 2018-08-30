import time
import sys
import math
import datetime, getopt
import pandas as pd



#import startegy
from MACD_Strategy import sMACD
#import datagathering for plotting performance
from plotter import plotter
#import binance
from binance.client import Client

def main(argv):

    client = Client("","")

    strategy = sMACD()

    #get data from binnace
    data= client.get_historical_klines(symbol='BTCUSDT', interval= '1h', start_str= '2017.06.16', end_str= '2018.08.27')
    #format
    data_df= pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    #init variables
    this = 0
    bestX =0
    bestY =0
    bestZ =0
    bestReturn =0
    #start trying all combos
    for x in xrange(1,40):
		for y in xrange(1,40):
			for z in xrange(1,60):
	
				print "running......" + str(x)+ " " + str(y) + " " + str(z)

                #run the series
				this = strategy.run(x,y,z,data_df)    
				
                #update new best performance
				if this>bestReturn:
					bestX = x
					bestY = y
					bestZ = z
					bestReturn = this
					print "new Best: "+ str(bestReturn )
	
    #run plotting 
    plt = plotter()
    plt.plot(bestX,bestY,bestZ,data_df)

    #at the end print best result       
    print "best return: " + str(bestReturn )
    print "best x: " + str(bestX )
    print "best y: " + str(bestY )
    print "best z: " + str(bestZ )
    
if __name__ == "__main__":
    main(sys.argv[1:])
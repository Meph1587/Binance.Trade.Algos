import time
import sys
import math
import datetime, getopt
import pandas as pd



#import startegy
from HeikinAshiTrue import HeikinStrategy
#import datagathering for plotting performance
from plotter import plotter
#import binance
from binance.client import Client

def main(argv):

    client = Client("","")

    strategy = HeikinStrategy()

    timeframes = ["5m"]

    bestReturn = 0 

    for time in timeframes:

        #get data from binnace
        data = client.get_historical_klines(symbol = 'BTCUSDT', interval = time , start_str = '2017.08.17')
        #format
        data_df = pd.DataFrame(data, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
        
        data_df["Open time"] = data_df["Open time"]/1000

        this = 0
        
        print "running...... " + str(time)

        #run the series
        this = strategy.run(1,data_df)  

        print "return: " + str(this)

		
        #update new best performance
        if this>bestReturn:

            bestReturn = this
            bestTime = time
            print "new Best: " + str(bestReturn )

            print "Current Best: " + str(bestReturn ) + " " + str(time)
    	
    #run plotting 
    plt = plotter()
    plt.plot(1,data_df)

        #at the end print best result       
    print "best return: " + str(bestReturn )
    print "best time: " + str(bestTime )
  
    
if __name__ == "__main__":
    main(sys.argv[1:])
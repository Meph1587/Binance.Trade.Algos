import time
import sys
import math
import datetime, getopt
import pandas as pd



#import startegy
from HeikinAshi import HeikinStrategy
#import datagathering for plotting performance
from plotter import plotter
#import binance
from binance.client import Client

def getDataAndComputeHeikinAshi(_timeframe):

    client = Client("","")

    #get data from binnace
    data = client.get_historical_klines(symbol = 'BTCUSDT', interval = _timeframe , start_str = '2017.08.17')
    #format
    data_df = pd.DataFrame(data, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    #remove milliseconds from timestamp
    data_df["Open time"] = data_df["Open time"]/1000
    
    #Compute HeikinAshi candle: Open = (lastOpen + lastClose) / 2   ,   Close = (lastOpen + lastClose + lastHigh + lastLow) / 4
    data_df['HeikinOpen'] = (data_df['Open'].astype(float) + data_df['Close'].astype(float) ) / 2
    data_df['HeikinClose'] = (data_df['Open'].astype(float) + data_df['Close'].astype(float) + data_df['Low'].astype(float) + data_df['High'].astype(float)) / 4
    data_df["trend"] = "none"

    return data_df


def main(argv):

    strategy = HeikinStrategy()

    timeframes = ["2h"]

    bestReturn = 0 
    currentReturn = 0

    StartingCaptal = 1000.0

    for time in timeframes:

        #get Heikin-Ashi candles
        data_df = getDataAndComputeHeikinAshi(time)

        #pritn curent timeframe 
        print "running...... " + str(time)

        #run the series
        currentReturn = strategy.run(StartingCaptal,data_df)  

        #print result
        print "return: " + str(currentReturn)

		
        #update new best performance
        if currentReturn>bestReturn:

            bestReturn = currentReturn
            bestTime = time

            print "New Best: " + str(bestReturn ) + " " + str(time)
    	
    #run plotting 
    
    #get Heikin-Ashi candles of best timeframe
    data_df = getDataAndComputeHeikinAshi(bestTime)

    plt = plotter()
    plt.plot(bestTime,StartingCaptal,data_df)

  
    
if __name__ == "__main__":
    main(sys.argv[1:])
import time
import sys
import math
import datetime, getopt
import pandas as pd

class HeikinStrategy:
    def run(self,_length,data_df):
        
        #used to determin the state of the bot
        state = 0; #0 ready to buy, 1 ready to sell

        #money at start
        Capital = 500.0

        FirstPrice = 0

        #eth at start
        ETH = 0.0;

        firstRound = True
        secondRound = True

        Candle0 = None;
        Candle1 = None;
        Candle2 = None;

        #used to terminate when finished
        for i,Candle0 in data_df.iterrows():

            CurrPrice = float(Candle0["Open"])
            
            #takes first price
            if FirstPrice==0 :
                FirstPrice=CurrPrice
                #Capital = CurrPrice


            if firstRound == False and secondRound == False:

                Candle0['Open'] = (float(Candle1['Open']) + float(Candle1['Close']) ) / 2
                Candle0['Close'] = (float(Candle0['Open']) + float(Candle0['Close']) + float(Candle0['Low']) + float(Candle0['High'])) / 4



                if Candle0["Open"] < Candle0["Close"]:
                    Candle0["trend"] = "up"
                else:
                    Candle0["trend"] = "down"

                buyTrigger = (Candle1["trend"] == "up") & (Candle2["trend"] == "down")
                sellTrigger = (Candle1["trend"] == "down") & (Candle2["trend"] == "up")


                #state 0 -> wants to buy
                if state == 0:  
                    #check for MACD crossover
                    if buyTrigger:

                        BuyPrice=CurrPrice
                        state = 1
                        #execute buy
                        ETH = Capital/float(CurrPrice) 
                        ETH = ETH*0.999 #trading fee of 0.1% = 1/1000
                        #CurrStopLoss = float(CurrPrice)*_Limit
                        Capital = 0;
                        #print "::::::::::::::::::::::::::::::::::::BUY  " + str( CurrPrice )
                        
                
                #state 1 -> wants to sell
                if state==1:
                    #check for MACD crossover
                    if sellTrigger:
                        state=0;
                        #execute sell
                        Capital=float(CurrPrice)*ETH
                        Capital = Capital*0.999 #trading fee of 0.1%
                        #print "::::::::::::::::::::::::::::::::::::SELL  " + str( CurrPrice )
                        #print "Profit on trade: ", CurrPrice-BuyPrice

            Candle2 = Candle1
            Candle1 = Candle0

            if firstRound == True:
                firstRound = False
                Candle2 = Candle0
                Candle2['Open'] = (float(Candle0['Open']) + float(Candle0['Close']) ) / 2
                Candle2['Close'] = (float(Candle0['Open']) + float(Candle0['Close']) + float(Candle0['Low']) + float(Candle0['High'])) / 4

                print "started... -2"

            if firstRound == False and secondRound == True:
                secondRound = False
                Candle1 = Candle0
                Candle1['Open'] = (float(Candle2['Open']) + float(Candle2['Close']) ) / 2
                Candle1['Close'] = (float(Candle0['Open']) + float(Candle0['Close']) + float(Candle0['Low']) + float(Candle0['High'])) / 4

                if Candle1["Open"] < Candle1["Close"]:
                    Candle1["trend"] = "up"
                else:
                    Candle1["trend"] = "down"

                print "started... -1 "
            
            

            



        #return performance 
        return float(CurrPrice)*ETH;
'''

'''
                


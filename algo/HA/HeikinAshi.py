import time
import sys
import math
import datetime, getopt
import pandas as pd

class HeikinStrategy:
    def run(self,_startingCapital,data_df):
        
        #used to determin the state of the bot
        state = 0; #0 ready to buy, 1 ready to sell

        #money at start
        Capital = _startingCapital


        FirstPrice = 0

        #crypto at start
        Crypto = 0.0;

        firstRound = True

        lastCandles = None;

        #used to terminate when finished
        for i,Candle in data_df.iterrows():

            CurrPrice = float(Candle["Open"])

            #takes first price
            if FirstPrice==0 :
                FirstPrice=CurrPrice

            #get current trend
            if Candle["HeikinOpen"] < Candle["HeikinClose"]:
                Candle["trend"] = "up"
            else:
                Candle["trend"] = "down"

            #in first rounddo nothing
            if firstRound == True:
                firstRound = False
                lastCandles = Candle
                print "started..."
            

            if firstRound == False: 

                #compare currend trend agains trend of last candle
                buyTrigger = (Candle["trend"] == "up") & (lastCandles["trend"] == "down")
                sellTrigger = (Candle["trend"] == "down") & (lastCandles["trend"] == "up")


                #state 0 -> wants to buy
                if state == 0:  
                    
                    if buyTrigger:

                        BuyPrice = CurrPrice
                        #set state to selling
                        state = 1

                        #execute buy
                        Crypto = Capital/float(CurrPrice) 
                        Crypto = Crypto*0.999 #trading fee of 0.1% = 1/1000
                        Capital = 0;
                        
                
                #state 1 -> wants to sell
                if state==1:

                    if sellTrigger:
                        #set state to buying
                        state=0;

                        #execute sell
                        Capital=float(CurrPrice)*Crypto
                        Capital = Capital*0.999 #trading fee of 0.1%


            #save current candle for next round
            lastCandles = Candle

        #return performance 
        return float(CurrPrice)*Crypto;
'''

'''
                


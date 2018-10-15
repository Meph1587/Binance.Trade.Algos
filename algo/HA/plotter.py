import time
import sys
import math
import datetime, getopt
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client


class plotter:
    def plot(self,_time,_startingCapital,data_df):


        strategy = HeikinAshi_plott()
        this, that = strategy.run(_startingCapital,data_df)

        #compute all trades
        data_df['Open time']= pd.to_datetime(data_df['Open time'], unit='ms')
        time= data_df['Open time']

        #plot everything
        plt.plot(time,that,'b',label="Price BTC")
        plt.plot(time,this,'r',label="Capital on Timeframe: " + _time)
        plt.legend()
        plt.grid(True)
        plt.show()

#same as other but saves balance and prints trades
class HeikinAshi_plott:
    def run(self,_startingCapital,data_df):
        
        #used to determin the state of the bot
        state = 0; #0 ready to buy, 1 ready to sell

        #money at start
        Capital = _startingCapital

        FirstPrice = 0

        #eth at start
        ETH = 0.0;

        #used for performance analysis
        highestGain=0;
        highestLost=0;
        tradesGood=[];
        tradesBad=[];

        firstRound = True

        lastCandles = None;

        balances = pd.DataFrame(columns=['Capital'])
        price = pd.DataFrame(columns=['Price'])

        #used to terminate when finished
        for i,Candle in data_df.iterrows():

            CurrPrice = float(Candle["Open"])

            balances = balances.append({'Capital':max(Capital, ETH*CurrPrice)}, ignore_index=True)
            price = price.append({'Price':CurrPrice}, ignore_index=True)


            #takes first price
            if FirstPrice==0 :
                FirstPrice=CurrPrice
                #Capital = CurrPrice

            if Candle["HeikinOpen"] < Candle["HeikinClose"]:
                Candle["trend"] = "up"
            else:
                Candle["trend"] = "down"

            if firstRound == True:
                firstRound = False
                lastCandles = Candle
                print "started..."
            
            if firstRound == False: 

                buyTrigger = (Candle["trend"] == "up") & (lastCandles["trend"] == "down")
                sellTrigger = (Candle["trend"] == "down") & (lastCandles["trend"] == "up")

                #state 0 -> wants to buy
                if state == 0:  
                    #check for MACD crossover
                    if buyTrigger:

                        capitalBefore=Capital

                        state = 1
                        #execute buy
                        ETH = Capital/float(CurrPrice)
                        ETH = ETH*0.999

                        Capital = 0;
                        print "::::::::::::::::::::::::::::::::::::BUY "+str(CurrPrice) + " " + str(datetime.utcfromtimestamp(Candle["Open time"]).strftime('%Y-%m-%d %H:%M:%S'))
                        
                        
                
                #state 1 -> wants to sell
                if state==1:
                    #check for MACD crossover
                    if sellTrigger:


                        state=0;
                        #execute sell
                        Capital=float(CurrPrice)*ETH 
                        Capital = Capital*0.999 #trading fee of 0.1 % = 1/1000
                        
                        print "::::::::::::::::::::::::::::::::::::SELL "+str(CurrPrice) + " " + str(datetime.utcfromtimestamp(Candle["Open time"]).strftime('%Y-%m-%d %H:%M:%S'))
                        #check if new best/worst trade
                        if(float(((Capital/capitalBefore)*100)-100))>highestGain:
                            highestGain=float(((Capital/capitalBefore)*100)-100)
                        if(float(((Capital/capitalBefore)*100)-100))<highestLost:
                            highestLost=float(((Capital/capitalBefore)*100)-100)

                        print "Profit on trade: " +  str(((Capital/capitalBefore)*100)-100)+ "%"
                        if(Capital-capitalBefore>=0):
                            tradesGood.append(float(((Capital/capitalBefore)*100)-100));
                        else:
                            tradesBad.append(float(((Capital/capitalBefore)*100)-100))


            #save candle for later comparison
            lastCandles = Candle

          
        print "Starts with " + str(_startingCapital)+ ", ends with: " + str(CurrPrice*ETH)
        print "Buy-and-Hold strategy ends with: "+str(CurrPrice*(_startingCapital/FirstPrice));
        print "Profit :"+str((((CurrPrice*ETH)/_startingCapital)*100)-100) + "%"
        print "Compared against buy-and-hold :"+ str(((CurrPrice*ETH)/(CurrPrice*(_startingCapital/FirstPrice)))*100)+ "%"
        print "best trade :"+str(highestGain)  + "%"
        print "worst trade :" + str(highestLost) + "%"
    
        summ=0
        for l in tradesGood:
            summ+=l
        print "Avarage good trade :"+ str(summ/len(tradesGood)) + "%"
        print "Number of good trades :"+ str(len(tradesGood)) 
        summ=0
        for k in tradesBad:
            summ+=k
        print "Avarage bad trade :"+ str(summ/len(tradesBad)) + "%"
        print "Number of bad trades :"+ str(len(tradesBad))

        return balances, price 


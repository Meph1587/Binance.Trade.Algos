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
    def plot(self,length,data_df):


        strategy = HeikinAshi_plott()
        this, that = strategy.run(1,data_df)

        #compute all trades
        data_df['Open time']= pd.to_datetime(data_df['Open time'], unit='ms')
        time= data_df['Open time']

        #plot everything
        plt.plot(time,that,'b',label="Price BTC")
        plt.plot(time,this,'r',label="Capital")
        plt.legend()
        plt.grid(True)
        plt.show()

#same as other but saves balance and prints trades
class HeikinAshi_plott:
    def run(self,_length,data_df):
        
        #used to determin the state of the bot
        state = 0; #0 ready to buy, 1 ready to sell

        #money at start
        Capital = 500.0

        FirstPrice = 0

        ETH = 0.0;

        firstRound = True
        secondRound = True

        Candle0 = None;
        Candle1 = None;
        Candle2 = None;

        #used for performance analysis
        highestGain=0;
        highestLost=0;

        tradesGood=[];
        tradesBad=[];

        balances = pd.DataFrame(columns=['Capital'])
        price = pd.DataFrame(columns=['Price'])


        for i,Candle0 in data_df.iterrows():

            CurrPrice = float(Candle0["Open"])

            balances = balances.append({'Capital':max(Capital, ETH*CurrPrice)}, ignore_index=True)
            price = price.append({'Price':CurrPrice}, ignore_index=True)

            
            #takes first price
            if FirstPrice==0 :
                FirstPrice=CurrPrice
                #Capital = CurrPrice


            if firstRound == False and secondRound == False:

                Candle0['Open'] = (float(Candle0['Open']) + float(Candle0['Close']) ) / 2
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

                        capitalBefore=Capital
                        stopLoss = Candle1["Low"]

                        state = 1
                        #execute buy
                        ETH = Capital/float(CurrPrice)
                        ETH = ETH*0.999

                        Capital = 0;
                        print "::::::::::::::::::::::::::::::::::::BUY  " + str( CurrPrice )+ " " + str(datetime.utcfromtimestamp(Candle0["Open time"]).strftime('%Y-%m-%d %H:%M:%S'))
                        
                        
                
                #state 1 -> wants to sell
                if state==1:
                    #check for MACD crossover
                    if sellTrigger :
                        state=0;
                        #execute sell
                        Capital=float(CurrPrice)*ETH 
                        Capital = Capital*0.999 #trading fee of 0.1 % = 1/1000
                        
                        print "::::::::::::::::::::::::::::::::::::SELL "+str(CurrPrice) + " " + str(datetime.utcfromtimestamp(Candle0["Open time"]).strftime('%Y-%m-%d %H:%M:%S'))
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
                Candle1['Open'] = (float(Candle0['Open']) + float(Candle0['Close']) ) / 2
                Candle1['Close'] = (float(Candle0['Open']) + float(Candle0['Close']) + float(Candle0['Low']) + float(Candle0['High'])) / 4

                if Candle1["Open"] < Candle1["Close"]:
                    Candle1["trend"] = "up"
                else:
                    Candle1["trend"] = "down"

          
        print "Starts with 500, ends with: " + str(CurrPrice*ETH)
        print "Buy-and-Hold strategy ends with: "+str(CurrPrice*(500.0/FirstPrice));
        print "Profit :"+str((((CurrPrice*ETH)/500.0)*100)-100) + "%"
        print "Compared against buy-and-hold :"+ str(((CurrPrice*ETH)/(CurrPrice*(500.0/FirstPrice)))*100)+ "%"
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




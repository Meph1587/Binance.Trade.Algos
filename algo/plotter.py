import time
import sys
import math
import datetime, getopt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client


class plotter:
    def plot(self,x,y,z,data_df):


        strategy = MACD_Plott()
        this = strategy.run(x,y,z,data_df)

        #compute all trades
        data_df['Open time']= pd.to_datetime(data_df['Open time'], unit='ms')
        time= data_df['Open time']

        #plot everything
        plt.plot(time,this,'r',label="settings: "+str(x)+ ", "+str(y)+ ", "+str(z) )
        plt.legend()
        plt.grid(True)
        plt.show()
#same as other but saves balance and prints trades
class MACD_Plott:
    def run(self,VShort,VLong,VSignal,data_df):

        #create conenction
        Short=VShort;
        Long=VLong;
        Signal=VSignal;
        
        #used to determin the state of the bot
        state = 0; #0 ready to buy, 1 ready to sell

        #money at start
        Capital = 10000.0;

        #eth at start
        ETH = 0.0;

        #used for performance analysis
        highestGain=0;
        highestLost=0;
        #price at which buys in first time
        FirstPrice=0;

        #used to calculate MovingAvarageConvergenceDivergence
        #12-exponential moving avarage
        lastShort= []
        EMAShort=0;

        #12-exponential moving avarage
        lastLong= []
        EMALong=0;

        #12-exponential moving avarage
        lastSignal= []
        EMASignal=0;
        # 1 bullish, 0 bearish
        MACDstate=1;

        #state of last mesuorments used for crossovers
        MACDstateLast=0;

        tradesGood=[];
        tradesBad=[];

        balances = pd.DataFrame(columns=['Capital'])

        #used to terminate when finished
        for CurrPrice in data_df["Close"]:

            CurrPrice=float(CurrPrice)

            balances = balances.append({'Capital':max(Capital, ETH*CurrPrice)}, ignore_index=True)

            #takes first price
            if FirstPrice==0 :
                FirstPrice=CurrPrice


            #MACD is calculated : MACDline- SignalLine
                #MACDline is 12EMA-26EMA
                #SignalLine is 9EMA of MACD

            #getting 12ExponentialMovingAvarage
                #First 12times just get data
            if len(lastShort) <Short:
                lastShort.append(float(CurrPrice))
                #compute StandartMovingAvarage from first 12 prices
            if len(lastShort) == Short:
                del lastShort[0] # remove oldes
                lastShort.append(float(CurrPrice)) # add current price
                summ=0
                for i in lastShort:
                    summ = summ + i
                EMAShort=summ/Short; # get avarage of last 12 


            
            #sam ething aas for 12EMA
            if len(lastLong) <Long:
                lastLong.append(float(CurrPrice))

            if len(lastLong) == Long:
                del lastLong[0]
                lastLong.append(float(CurrPrice))
                summ=0
                for i in lastLong:
                    summ= summ+ i
                EMALong=summ/Long;


            #if data of last 26 times is here:
            if(EMALong!=0):

                #compute 9EMA but instead of price use MACDline
                if len(lastSignal) <Signal:
                    lastSignal.append(float(EMAShort-EMALong))  #EMA12-EMA26 = MACDline

                if len(lastSignal) == Signal:
                    del lastSignal[0]
                    lastSignal.append(float(EMAShort-EMALong))
                    summ=0
                    for i in lastSignal:
                        summ+=i
                    EMASignal=summ/Signal;



            #if data for EMA9 is here 
            if(EMASignal!=0):

                #get lines
                MACDline=EMAShort-EMALong
                SignalLine=EMASignal

                #get MACD by applying formula
                MACD= MACDline-SignalLine;
                #check if bullish or bearish
                if(MACD>0):
                    MACDstate=1

                if(MACD<0):
                    MACDstate=0

                #if(MACDstate!=MACDstateLast):
                   # print "Cross",MACD, CurrPrice


                #state 0 -> wants to buy
                if state == 0:  
                    #check for MACD crossover
                    if MACDstate!=MACDstateLast :
                        #update latest MACD
                        MACDstateLast=MACDstate
                        #set state to be ready to sell
                        BuyPrice=CurrPrice
                        state = 1
                        #execute buy
                        ETH = Capital/float(CurrPrice)
                        ETH = ETH*0.999
                        Capital = 0;
                        print "::::::::::::::::::::::::::::::::::::BUY "+str(CurrPrice)
                        
                

                #state 1 -> wants to sell
                if state==1:
                    #check for MACD crossover
                    if MACDstate!=MACDstateLast  :
                        #update MACD
                        MACDstateLast=MACDstate
                        #set state back to for next buy
                        state=0;
                        #execute sell
                        Capital=float(CurrPrice)*ETH 
                        Capital = Capital*0.999 #trading fee of 0.1 % = 1/1000
                        
                        print "::::::::::::::::::::::::::::::::::::SELL "+str(CurrPrice)
                        #check if new best/worst trade
                        if(CurrPrice-BuyPrice)>highestGain:
                            highestGain=(CurrPrice-BuyPrice)
                        if(CurrPrice-BuyPrice)<highestLost:
                            highestLost=(CurrPrice-BuyPrice)

                        print "Profit on trade: ", CurrPrice-BuyPrice
                        if(CurrPrice-BuyPrice>=0):
                            tradesGood.append(float(CurrPrice-BuyPrice));
                        else:
                            tradesBad.append(float(CurrPrice-BuyPrice))

                #set current MACD state to be Last in next round
        		MACDstateLast=MACDstate

        return balances
        '''    
		print "ends with: " + str(CurrPrice*ETH)
	    print "Buy-and-Hold strategy ends with: "+str(CurrPrice*(10000.0/FirstPrice))+"/10'000";
	    print "Profit :"+str((((CurrPrice*ETH)/10000.0)*100)-100) + "%"
	    print "Compared against buy-and-hold :"+ str(((CurrPrice*ETH)/(CurrPrice*(10000.0/FirstPrice)))*100)+ "%"
	    print "best trade :"+str(highestGain)
	    print "worst trade :" + str(highestLost)
	    summ=0
	    for l in tradesGood:
	        summ+=l
	    #print ("Avarage good trade :", summ/len(tradesGood))
	    summ=0
	    for k in tradesBad:
	        summ+=k
	    #print ("Avarage bad trade :", summ/len(tradesBad))
	    runs=False;
        '''

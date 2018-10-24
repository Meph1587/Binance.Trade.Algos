import time
import sys
import math
import datetime, getopt
import pandas as pd
from binance.client import Client

client = Client("","")

class trader:

    
    def getLastCandleOpen(_pair):
        data = client.get_historical_klines(symbol=_pair, interval= '2h', start_str= '4 hour ago UTC')
        data_df= pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
        return str(data_df['Open'][0]);


    def makeTradeBuy(_pair,_toSell,_type):
        _price = float(client.get_ticker(symbol=_pair)["lastPrice"])
        _balance = float(client.get_asset_balance(asset=_toSell)["free"])
        _quantity =  round(_balance/_price,5) - 0.00002 #round and than subtract to avoid rounding to value higher than balance
        print _quantity
        print _balance/_price
        order = client.create_test_order(
            symbol = _pair,
            side = "BUY",
            type = "LIMIT",
            timeInForce = "GTC",
            quantity = _quantity,
            price = _price
        )
        print order
        return order 


    print getLastCandleOpen("BTCUSDT")
    makeTradeBuy("BTCUSDT","USDT", "BUY")

    #def SetBuyOrder(_price, _type, )
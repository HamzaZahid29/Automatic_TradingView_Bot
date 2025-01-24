import sys
import os
# add main directoty of the project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# import binace api class
from tradingbinance.Binaceapi import BinanceApi

# call class method to extract price
def give_me_symbol_price(symbol):
    try:
        Api=BinanceApi()
        price=Api.getcryptoprice(symbol)
        return price
    except Exception as e:
        print('Got An Exception By give_me_symbol_price()',e)    
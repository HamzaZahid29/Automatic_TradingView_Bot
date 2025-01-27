import sys
import os
# add main directoty of the project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# import config file
from config.config import Config
from helper.Log import insertlog
import math
from binance.client import Client


class BinanceApi:
    # generating constructor
    def __init__(self):
        self.sec=Config.api_sec
        self.key=Config.api_key
        self.client=Client(self.key,self.sec,testnet=True)
    # check crypto price    
    def getcryptoprice(self,symbol):
        btc_price=self.client.get_symbol_ticker(symbol=symbol)
        return btc_price.get('price') 
        
    # check balance    
    def check_balance(self):
        account_info = self.client.get_account()
        balances = account_info['balances']
        all_assets=[]
        for balance in balances:
            asset = balance['asset']  
            free = balance['free']   
            all_assets.append({asset:free})
        return all_assets    


    # spot trade methods---------------------------------------------------------------    
    # creating method to place order
    def create_order_spot(self,data_dict):
        try:
          symbol=data_dict.get('Symbol')
          Quantity=data_dict.get('Quantity')
          signal=data_dict.get('Signal').lower()
          price=float(data_dict.get('Price'))
          min_notional = 10  # Assuming $10 as the minimum notional
          min_quantity = math.ceil(min_notional / price) 
          if 'Buy'.lower() in signal:
           try:
               order=self.client.create_order(symbol=symbol,side=Client.SIDE_BUY,type='MARKET', quantity=min_quantity)
               print('the order created')
               insertlog(data_dict)
               return order
           except Exception as e:
               print('Bug In Spot For Buy',e)    

          elif 'sell' in signal:
            #   execute sell Api    
            try:
                order=self.client.create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=min_quantity)
                print('Market Sell Order successfully created!')
                insertlog(data_dict)
                return order
            except Exception as e:
                print('error while creating sell spot order',e)    
            
        except Exception as e:
            print('Facing Issue While Create Order For Spot',e)    

    # future trade method-------------------------------------------------------------
    # creating method place order for future

    def create_order_future(self,data_dict):
        try:
            symbol=data_dict.get('Symbol')
            symbol_price=self.getcryptoprice(symbol)
            Quantity=data_dict.get('Quantity')
            signal=data_dict.get('Signal').lower()
            price=float(data_dict.get('Price'))
            min_notional = 10  # Assuming $10 as the minimum notional
            min_quantity = math.ceil(min_notional / float(price))
            take_profit_price = float(data_dict.get('Price'))* 1.02  # Example: 2% above current price
            stop_loss_price = (float(data_dict.get('Price'))* 0.98 )+1
            if 'Buy'.lower() in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_BUY,type='MARKET',quantity=min_quantity)
                    print(order)
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('Got An Error For Buy Future',e)    

            elif 'Sell'.lower() in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=self.client.SIDE_SELL,type='MARKET',quantity=min_quantity)
                    print('order created for sell')
                    insertlog(order)
                    return order
                except Exception as e:
                    print('Got An Exeption as futures sell',e)    

            elif 'stp' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side='SELL',type='STOP_MARKET',quantity=min_quantity,stopPrice=int(stop_loss_price))
                    print('stp order placed')
                    insertlog(order)
                    return order
                except Exception as e:
                    print('got an expenstion in future stp trade',e)            

            elif 'btp' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,type=Client.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,side='BUY',quantity=min_quantity,take_profit_price=take_profit_price,stopPrice=int(stop_loss_price))
                    print('btp order trigger')
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('got an expenstion in future btp trade',e)            
            elif 'ssl' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,type=Client.ORDER_TYPE_STOP_LOSS_LIMIT,side='SELL',quantity=min_quantity,stopPrice=int(stop_loss_price), price=int(stop_loss_price))
                    print('ssl order trigger')
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('got an expenstion in future ssl trade',e)
            elif 'bsl' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,type=Client.ORDER_TYPE_STOP_LOSS_LIMIT,side='BUY',quantity=min_quantity,stopPrice=int(stop_loss_price), price=int(stop_loss_price))
                    print('ssl order trigger')
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('got an expenstion in future ssl trade',e)                    
        except Exception as e:
            print('Facing Issue While Create Order For Future',e)    

   
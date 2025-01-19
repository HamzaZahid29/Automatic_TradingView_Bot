import sys
import os
# add main directoty of the project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# import config file
from config import api_key,api_sec
from binance.client import Client

class BinanceApi:
    # generating constructor
    def __init__(self):
        self.sec=api_sec
        self.key=api_key
        self.client=Client(self.key,self.sec)
    # check crypto price    
    def getcryptoprice(self):
        btc_price=self.client.get_symbol_ticker(symbol="BTCUSDT")
        print(btc_price)
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
          signal=data_dict.get('Signal').lower()
          price=data_dict.get('Price')
          quantity=data_dict.get('Quantity')
          symbol=data_dict.get('Symbol')

          if 'buy' in signal:
            try:
                #   execute buy Api
                order=self.client.create_order(symbol=symbol,side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
                print('Order Created SuccessFully......')
                return order
            except Exception as e:
                print('error while creating buy spot order')    

          elif 'sell' in signal:
            #   execute sell Api    
            try:
                order=self.client.create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
                print('Market Sell Order successfully created!')
                return order
            except Exception as e:
                print('error while creating sell spot order')    

          elif 'btp' in signal:
              try:
                  order=self.client.order_limit_sell(symbol=symbol,quantity=quantity,price=str(price))
                  print("Spot BTP order created:")
                  return order
              except Exception as e:
                  print('got an exception while btp spot order',e)            

          elif 'stp' in signal:
              try:
                  order=self.client.order_limit_buy(symbol=symbol,quantity=quantity,price=str(price))
                  print("Spot STP order created:")
                  return order
              except Exception as e:
                  print('got an exception while stp order spot',e)             
                
        except Exception as e:
            print('Facing Issue While Create Order For Spot',e)    

    # future trade method-------------------------------------------------------------
    # creating method place order for future
    def create_order_future(self,data_dict):
        try:
            signal=data_dict.get('Signal').lower()
            price=data_dict.get('Price')
            quantity=data_dict.get('Quantity')
            symbol=data_dict.get('Symbol')
            # define take profit or loss profit
            # 2 % above
            take_profit_price=price*1.02
            # 2% below
            stop_loss_price=price*0.98

            if 'buy' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.FUTURE_ORDER_TYPE_MARKET,quantity=quantity)
                    print('Futures Order Successful:')
                    return order
                except Exception as e:
                    print('Got Expection in future create order',e)    

            elif 'sell' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.FUTURE_ORDER_TYPE_MARKET,quantity=quantity)        
                    print('Futures Order Successful: for sell')
                    return order
                except Exception as e:
                    print('Got Expection in future create order sell ',e)    

            if 'btp' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_BUY,type=Client.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,quantity=quantity,stopPrice=take_profit_price)
                    print('BTP Order Created:')
                    return order
                except Exception as e:
                    print('got an expenstion in future btp trade',e)            

            if 'stp' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.FUTURE_ORDER_TYPE_STOP_MARKET,quantity=quantity,stopPrice=stop_loss_price)
                    print('STP Order Created:')
                    return order
                except Exception as e:
                    print('got an expenstion in future stp trade',e)            

        except Exception as e:
            print('Facing Issue While Create Order For Future',e)    


   

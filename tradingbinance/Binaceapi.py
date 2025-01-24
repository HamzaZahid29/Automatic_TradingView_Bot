import sys
import os
# add main directoty of the project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# import config file
from config.config import Config
from helper.Log import insertlog
from binance.client import Client

class BinanceApi:
    # generating constructor
    def __init__(self):
        self.sec=Config.api_sec
        self.key=Config.api_key
        self.client=Client(self.key,self.sec)
    # check crypto price    
    def getcryptoprice(self,symbol):
        btc_price=self.client.get_symbol_ticker(symbol=symbol)
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
                insertlog(data_dict)
                return order
            except Exception as e:
                print('error while creating buy spot order')    

          elif 'sell' in signal:
            #   execute sell Api    
            try:
                order=self.client.create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
                print('Market Sell Order successfully created!')
                insertlog(data_dict)
                return order
            except Exception as e:
                print('error while creating sell spot order')    
           
                
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
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('Got Expection in future create order',e)    

            elif 'sell' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.FUTURE_ORDER_TYPE_MARKET,quantity=quantity)        
                    print('Futures Order Successful: for sell')
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('Got Expection in future create order sell ',e)    

            elif 'btp' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_BUY,type=Client.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,quantity=quantity,stopPrice=take_profit_price)
                    print('BTP Order Created:')
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('got an expenstion in future btp trade',e)            

            elif 'stp' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_SELL,type=Client.FUTURE_ORDER_TYPE_STOP_MARKET,quantity=quantity,stopPrice=stop_loss_price)
                    print('STP Order Created:')
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('got an expenstion in future stp trade',e)             
            elif 'bsl' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,side=Client.SIDE_BUY,type=Client.FUTURE_ORDER_TYPE_STOP_MARKET,stopPrice=take_profit_price,
                quantity=quantity,               
                timeInForce="GTC" )
                    insertlog(data_dict)
                    print('order triggered for bsl')
                    return order
                except Exception as e:
                    print('got an exception while call api for bsl signal',e)            
            elif 'ssl' in signal:
                try:
                    order=self.client.futures_create_order(symbol=symbol,
            side=Client.SIDE_SELL,                # Selling to limit losses
            type=Client.FUTURE_ORDER_TYPE_STOP,          # Stop-Limit order type
            stopPrice=stop_loss_price,            # Trigger price
            price=price,                          # Limit price
            quantity=quantity,                    # Quantity to sell
            timeInForce="GTC" )
                    print('ssl order created')
                    insertlog(data_dict)
                    return order
                except Exception as e:
                    print('Got An Exception While SSL order trigger',e)            
            else:
                print('Invalid Signal')
        except Exception as e:
            print('Facing Issue While Create Order For Future',e)    



   

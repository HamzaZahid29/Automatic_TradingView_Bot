from tradingbinance.Binaceapi  import BinanceApi

# make function for all
def main_api_container(data):
    Api=BinanceApi()        
    # calling trade according to scenerio
    if data.get('type') == 'spot':
        Api.create_order_spot(data)
        
    else:
        Api.create_order_future(data) 
        
from binance.client import Client

API_KEY = "ba4aa14ee45b51e9f7a7147cd804189fb0c7901c37965cb906053ec8eb76f2f1"
SECRET_KEY = "56791c93b7344865f7d2af8dd2a7b53664309d69c65bc2a813e372b764979656"
client = Client(API_KEY, SECRET_KEY, testnet=True)
print(client.futures_account())
print(client)
# Get the current price of a symbol
def get_crypto_price(symbol):
    btc_price = client.get_symbol_ticker(symbol=symbol)
    return btc_price.get('price')

# Check balances of all assets
def check_balance():
    account_info = client.futures_account()
    balances = account_info['balances']
    all_assets = []
    for balance in balances:
        asset = balance['asset']
        free = balance['free']
        all_assets.append({asset: free})
    return all_assets

# Get specific coin balance
def get_coin_balance(symbol):
    account_info = client.futures_account()
    print(account_info)
    for asset in account_info['assets']:
        if asset['asset'] == symbol:
            free_balance = asset['free']
            locked_balance = asset['locked']
            return f"Balance for {symbol}: {free_balance} free, {locked_balance} locked"
    return f"No balance found for {symbol}"

# Get the precision for price and quantity for a symbol
def get_precision(symbol):
    info = client.get_symbol_info(symbol)
    price_precision = info['filters'][0]['tickSize']
    quantity_precision = info['filters'][1]['stepSize']
    price_decimals = len(price_precision.split('.')[1]) if '.' in price_precision else 0
    quantity_decimals = len(quantity_precision.split('.')[1]) if '.' in quantity_precision else 0
    return price_decimals, quantity_decimals

# Round the values to match Binance's precision
def round_to_precision(value, decimals):
    return round(value, decimals)

# Place an order with the correct price and quantity precision
def place_order(symbol, quantity, price):
    price_precision, quantity_precision = get_precision(symbol)
    
    # Round the price and quantity to the correct precision
    rounded_price = round_to_precision(price, price_precision)
    rounded_quantity = round_to_precision(quantity, quantity_precision)
    
    print(f"Placing order for {symbol}:")
    print(f"Price: {rounded_price}, Quantity: {rounded_quantity}")
    
    # Example of placing a limit order (BUY order)
    order = client.order_limit_buy(
        symbol=symbol,
        quantity=rounded_quantity,
        price=str(rounded_price)
    )
    return order

# Main function to use the flow
def testing_flow():
    symbol = "XRPUSDT"
    quantity=1  
    current_price = get_crypto_price(symbol)
    print(f"Current price of {symbol}")
    
    # Check balance for BTC
    # balance = get_coin_balance(symbol)
    # print(balance)
    
    # Place order with the correct precision
    order = place_order(symbol, quantity,current_price)
    print("Order placed:", order)

# Run the testing flow
testing_flow()




from binance.client import Client

API_KEY = "your_api_key_here"
SECRET_KEY = "your_api_secret_here"
client = Client(API_KEY, SECRET_KEY)

# Spot Buy (Market)
def spot_buy(symbol, quantity):
    order = client.order_market_buy(
        symbol=symbol,
        quantity=quantity
    )
    return order

# Futures Buy (Market)
def futures_buy(symbol, quantity):
    order = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        type='MARKET',
        quantity=quantity
    )
    return order

# Spot Sell (Market)
def spot_sell(symbol, quantity):
    order = client.order_market_sell(
        symbol=symbol,
        quantity=quantity
    )
    return order

# Futures Sell (Market)
def futures_sell(symbol, quantity):
    order = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='MARKET',
        quantity=quantity
    )
    return order

# Spot Take Profit (Limit Sell)
def spot_take_profit(symbol, quantity, price):
    order = client.order_limit_sell(
        symbol=symbol,
        quantity=quantity,
        price=price
    )
    return order

# Futures Take Profit (Limit Sell)
def futures_take_profit(symbol, quantity, price):
    order = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='LIMIT',
        quantity=quantity,
        price=price,
        timeInForce='GTC'
    )
    return order

# Spot Stop Loss (Stop Market Sell)
def spot_stop_loss(symbol, quantity, stop_price, price):
    order = client.order_stop_market_sell(
        symbol=symbol,
        quantity=quantity,
        stopPrice=stop_price,
        price=price
    )
    return order

# Futures Stop Loss (Stop Market Sell)
def futures_stop_loss(symbol, quantity, stop_price, price):
    order = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='STOP_MARKET',
        quantity=quantity,
        stopPrice=stop_price,
        price=price
    )
    return order

symbol = "XRPUSDT"
quantity = 1
price = 2.8  
stop_price = 1.05  

print(spot_buy(symbol, quantity))

print(futures_buy(symbol, quantity))

print(spot_take_profit(symbol, quantity, price))

print(futures_take_profit(symbol, quantity, price))

print(spot_stop_loss(symbol, quantity, stop_price, price))

# Futures Stop Loss
print(futures_stop_loss(symbol, quantity, stop_price, price))

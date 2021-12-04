import time
import pykorbit
import datetime

access = ""
secret = ""

korbit = pykorbit.Korbit(access, secret )


def get_target_price(ticker, k):
    df = pykorbit.get_ohlc(ticker, timeunit="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    df = pykorbit.get_ohlc(ticker, timeunit="day", period=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    balances = korbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    return pykorbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

korbit = pykorbit.Korbit(access, secret)
print("autotrade start")


while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("BTC", 0.7) 
            current_price = get_current_price("BTC") 
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    korbit.buy_market_order("BTC", krw*0.9985) 
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                korbit.sell_market_order("BTC", btc*0.9985) 
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

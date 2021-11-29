import time
import pykorbit
import datetime

access = "aa"
secret = "aa"
korbit = pykorbit.Korbit(access, secret )


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pykorbit.get_ohlc(ticker, timeunit="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pykorbit.get_ohlc(ticker, timeunit="day", period=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = korbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pykorbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
korbit = pykorbit.Korbit("De9YF173EUpa9PhqMVdzRGFDgaMm9GZsBL59LSe6j6cmjwzhbJnRDpsSJkhTI", "Sb4M9pn7PThhCvczNCOfvCeLxZqHK0bM6rG1qsQZwokZmPrXGuJNFKJhR60kM")
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("BTC") #was KRW-BTC
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("BTC", 0.5)  #was KRW-BTC
            current_price = get_current_price("BTC")  #was KRW-BTC
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    korbit.buy_market_order("BTC", krw*0.9985)  #was KRW-BTC
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                korbit.sell_market_order("BTC", btc*0.9985)  #was KRW-BTC
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

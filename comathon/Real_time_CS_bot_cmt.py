import random
import comathon as cmt
import time, datetime

print("Test")
print("Test")
print("Test")
print("Test")


access_key = '5uJbvx4hQwArlLbKdxzHjYGWVtEcEaeVKRCIvXXS'  # access key
secret_key = 'jRkeAOYYYOg7sK8PCxG9AFrBKfP4voqVVYg2oyWI'  # secret key
comathon_ID = "test003" #현재 test001, tst002, test003 가 등록되어 있음, 수정요청함

myAPI = cmt.Upbit(access_key, secret_key, comathon_ID)  # API 로그인 함수 호

print('')

ticker = cmt.get_tickers('KRW')
ini_bal = 3000000
start_date = '2023-02-18'

stop_loss = -50


# 원화잔고 작성
def get_krw_bal():
    while True:
        try:
            krw_bal = int(myAPI.get_balance())
            break
        except:
            pass
    return krw_bal

# 유효 코인장고 작성
bal_dict = {}
bal_ticker = []
def get_coin_bal():
    global bal_dict, ticker, bal_ticker
    bal_dict = {}
    bal_ticker = []
    while True:
        try:
            t_coin_bal = myAPI.get_balances()
            break
        except:
            pass
    for i in range(len(t_coin_bal)):
        if i >= 1:
            while True:
                try:
                    krw_name = 'KRW-' + t_coin_bal[i]['currency']
                    # print(krw_name)
                    if i > 0 and krw_name in ticker:
                        coin_bal = float(t_coin_bal[i]['balance'])
                        now_coin_price = cmt.get_current_price(krw_name)
                        coin_krw_bal = now_coin_price * coin_bal

                        # print(coin_krw_bal)
                        if coin_krw_bal > 10000:
                            bal_dict[krw_name] = coin_bal
                            bal_ticker.append(krw_name)
                    break
                except:
                    pass


scr_list = []
def get_scr_list():
    global ticker, scr_list

    scr_list = []
    for i in ticker:
        while True:
            try:

                ohlcv = cmt.get_ohlcv(i, interval='day', count=3)
                o0 = (ohlcv['open'].tolist())[-1]
                c0 = (ohlcv['close'].tolist())[-1]
                v0 = (ohlcv['volume'].tolist())[-1]
                v1 = (ohlcv['volume'].tolist())[-2]

                if (o0 * 0.95 > c0 or o0 * 1.05 < c0) and v1 * 3 < v0:
                    scr_list.append(i)

                break
            except:
                # print('get_scr_list_error')
                pass


#
now = datetime.datetime.now()
time_set = datetime.datetime(now.year, now.month, now.day)

start = time_set + datetime.timedelta(hours=8, seconds=59)
stop = start + datetime.timedelta(minutes=5)

while True:  # 시간 조정
    if start < now:
        break
    elif now < start:
        start = start - datetime.timedelta(hours=24)
        stop = stop - datetime.timedelta(hours=24)
    # print(start, stop)
while True: # 시간 조정
    if start > now:
        break
    elif now > start:
        start = start + datetime.timedelta(hours=24)
        stop = stop + datetime.timedelta(hours=24)


index = 0

# 테스트
# get_coin_bal()
# print(bal_ticker)
# avg_price = myAPI.get_avg_buy_price(bal_ticker[0])
# print(avg_price)

while True:

    try:
        now = datetime.datetime.now()        
        if start < now < stop:
            get_scr_list()
            random.shuffle(scr_list)
            get_coin_bal()
            krw = get_krw_bal()

            if len(bal_ticker) != 0:
                now_price = cmt.get_current_price(bal_ticker[0])
                avg_price = myAPI.get_avg_buy_price(bal_ticker[0])
                

                if (now_price > avg_price) or (now_price < avg_price * (1 + stop_loss/100)):

                    cmt.sell_market_order(myAPI, bal_ticker[0], 1)
                    time.sleep(3)

                    get_coin_bal()

            elif len(bal_ticker) == 0:

                if len(scr_list) > 0:

                    buy_amount = krw * 0.9995
                    cmt.buy_market_order(myAPI, scr_list[0], buy_amount)
                    time.sleep(3)

                    get_coin_bal()

                elif len(scr_list) == 0:
                    pass

            start = start + datetime.timedelta(hours=24)
            stop = stop + datetime.timedelta(hours=24)

        elif now > stop:

            start = start + datetime.timedelta(hours=24)
            stop = stop + datetime.timedelta(hours=24)

        index = index + 1

        if index % 100 == 0:
            check_server = cmt.server_alive(myAPI)
            print("Server Online : ", check_server)
            print("GAZUA, index = ", index)

        time.sleep(5)

    except:
        # print('Main Roof Error', now)
        pass
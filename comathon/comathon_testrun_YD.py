import pyupbit
import datetime
import time
import numpy as np
import pandas as pd
import csv
import threading
import comathon as cmt


#### Upbit API Info #########
# access_key = "PBJJMdbWmo1r58HTbiwDMfoYjft1f49Mb7KYlpTZ"
# secret_key = "nkN6sMNqUE7rj0WfLIjnY9XCXx5yCfQFvwCcuD3c"
# upbit = pyupbit.Upbit(access_key, secret_key)
#############################

hello = cmt.get_current_price('KRW-BTC')
print(hello)

######## Variables #####################################################################################################
time_delay = 60         ## delaying the loop by input time
time_instant = 0.02     ## delaying the data call from upbit
profit_rate = 1.05      ## profit rate
minimum_balance = 2000  ## minimum account balance to purchase coin
for_loop = 10000
buy_log = [0]
sell_log = [0]
ticker = ['KRW-ETH']
##  day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month
##  open  high  low  close  volume  value
candle = 1
itv = 'minute1'    ## interval
########################################################################################################################


###################### Basic Pyupbit Functions #########################################################################
#### 업비트 통신용 코드

# def current_time():
#     ct = datetime.datetime.now()
#     return ct
#
# def get_current_price(currency):
#     cp = round(pyupbit.get_current_price(currency), 1)
#     return cp
#
# def get_balance(currency_type):
#     balance = upbit.get_balance(ticker=currency_type)
#     return balance
#
# def buy_market_order(currency, buy_amount_won):
#     bc = upbit.buy_market_order(currency, buy_amount_won)
#     return bc
#
# def sell_market_order(currency):
#     amount = get_balance(currency)
#     sc = upbit.sell_market_order(currency, amount)
#     return sc
########################################################################################################################


######### Backup function, store traded coin list ######################################################################
#### 코인 거래기록을 csv 포맷의 파일로 저장

# reader = csv.reader(open('backup.csv', 'r'))
coin_dic = {}
# for row in reader:
#     k, v = row
#     coin_dic[k] = v
# print(coin_dic)

def backup(bors, coin_name):
    if bors == 'buy':
        coin_dic[coin_name] = get_current_price(coin_name)
        with open('backup.csv', 'w') as f:
            for key in coin_dic.keys():
                f.write("%s, %s\n" % (key, coin_dic[key]))
        print('from backup :', coin_dic)
        return coin_dic

    elif bors == 'sell':
        del coin_dic[coin_name]
        with open('backup.csv', 'w') as f:
            for key in coin_dic.keys():
                f.write("%s, %s\n" % (key, coin_dic[key]))
        print('New Current Account :', coin_dic)
        return coin_dic
########################################################################################################################


############ Log function ##############################################################################################
#### 매매 기록을 sell_log, buy_log variable 에 기록

def log(n):     ## 0 : check log, 1 : sell, 2 : buy, 3 : everything
    print('check log history : ', 'sell log :', sell_log, 'buy log :', buy_log)
    if n == 0:
        print('sell log : ', sell_log, 'last item is :', sell_log[-1])
        return sell_log[-1]

    elif n == 1:
        print('sell log : ', sell_log, 'last item is :', sell_log[-1])
        sell_history_price = get_current_price(ticker[0])
        sell_log.append(sell_history_price)
        print('sell log append : ', sell_log, 'last item is :', sell_log[-1])

        sell_log5 = pd.DataFrame({'Price': [sell_log[-1]], 'Time': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')]})
        sell_log5.to_csv(r'sell_log5.csv', mode='a', index=False, header=False)
        return sell_log[-1]

    elif n == 2:
        print('buy log : ', buy_log, 'last item is :', buy_log[-1])
        buy_log_price = get_current_price(ticker[0])
        buy_log.append(buy_log_price)
        print('buy log append : ', buy_log, 'last item is :', buy_log[-1])

        buy_log5 = pd.DataFrame({'Price': [buy_log[-1]], 'Time': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')]})
        buy_log5.to_csv(r'buy_log5.csv', mode='a', index=False, header=False)
        return buy_log[-1]

    elif n == 3:
        current_log = pd.DataFrame({'Price': [get_current_price(ticker[0])], 'Time': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')]})
        current_log.to_csv(r'current_price_log.csv', mode='a', index=False, header=False)

    else:
        print('log error')
########################################################################################################################


######################### Buy Signals ##################################################################################
#### 매수 시그널

def buying_signal_01(data):
    cpo = data['open']
    cpc = data['close']
    cpavg = (cpo+cpc)/2

    if cpavg[6] > cpavg[7] > cpavg[8] > cpavg[9]:
        print('Activate Signal 1')
        return 1
    else:
        print('    No signals to activate')
########################################################################################################################


########################## Selling Signals #############################################################################
#### 매도 시그널

def ma(data):
    cma_open = data['open']
    cma_close = data['close']
    cma_avg = np.around((cma_open + cma_close)/2, 1)
    cma_list = [cma_avg[0], cma_avg[1], cma_avg[2], cma_avg[3], cma_avg[4], cma_avg[5], cma_avg[6], cma_avg[7], cma_avg[8], cma_avg[9]]
    # print('cma_list : ', cma_list)

    numbers = cma_list
    window_size = 6

    numbers_series = pd.Series(numbers)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:]

    print('    MA : ', np.around(without_nans, 1))
    ma_last = without_nans[-1]
    ma_last2 = without_nans[-2]
    slope = (ma_last - ma_last2)/15
    print('    slope : ', np.around(slope, 2))

    if slope > 0:
        print('positive slope')
    else:
        print('negative slope')

    return slope
########################################################################################################################


#################### Trading Function ##################################################################################
#### 매매를 위해 loop형태로 run시킴. Buy signal과 Sell signal을 불러와 실질적인 업비트 매매를 하는 코드

def trading_coins():
    for i in range(for_loop):
        try:
            for coin_name in ticker:
                current_data = pyupbit.get_ohlcv(ticker[0], interval=itv, count=10)

                if (i+9) % candle == 0:
                    print('      BUYING LOOP')
                    if buying_signal_01(current_data) == 1:
                        print(f'Activate Signal, {coin_name}')

                        if coin_dic.get(coin_name):
                            print('  already have this coin')

                        elif get_balance('KRW') > minimum_balance:

                            print('check the current price with last sell price')
                            if (log(0) == 0) or (log(0) > get_current_price(coin_name)):

                                buy_price = get_current_price(coin_name)
                                buy_amount = (np.round(upbit.get_balance(ticker='KRW'), 0) - 5000)

                                print('--------------------------')
                                print(coin_name, ', BUY, Price :', buy_price, ', Time :', current_time())
                                # print(buy_market_order(coin_name, buy_amount))
                                print('--------------------------')

                                log(2)
                                bors = 'buy'
                                backup(bors, coin_name)

                            else:
                                print('last sale price is higher than current price')
                                pass
                        else:
                            print('Account has less than minimum balance')
                    else:
                        print(f'  Signal - Not Activated, {coin_name}')
                else:
                    print('skip to selling')

                log(3)                      ## writing every price
                time.sleep(time_instant)

                print('      SELLING LOOP')
                if coin_dic.get(coin_name):
                    print(f'  trying to sell {coin_name}')

                    if (float(get_current_price(coin_name)) > (float(coin_dic[coin_name]) * profit_rate)) & (ma(current_data) < 0):
                        time.sleep(time_instant)
                        sell_price = get_current_price(coin_name)
                        print('--------------------------')
                        print('Meet the profit rate and MA is negative slope')
                        print(coin_name, ', SELL, Price : ', sell_price, ', Time : ', current_time())
                        # print(sell_market_order(coin_name))
                        print('--------------------------')

                        log(1)
                        print('buy price was :', coin_dic[coin_name])

                        bors = 'sell'
                        backup(bors, coin_name)

                    elif (float(get_current_price(coin_name)) > (float(coin_dic[coin_name]) * profit_rate)) & (ma(current_data) >= 0):
                        print('Meet the profit rate but MA is positive slope')

                    else:
                        print(f'  {coin_name} does not meet the profit rate')
                else:
                    print(f'    No crypto to sell')
                    continue

            print(f'Loop Counter :', i)
            time.sleep(time_delay)

        except:
            print('Running Error')
            time.sleep(time_delay)
            continue
########################################################################################################################

########### Multi-Threading ############################################################################################
trading = threading.Thread(target = trading_coins)
trading.start()
########################################################################################################################
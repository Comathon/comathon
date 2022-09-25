import requests
import pyupbit


## Buy Function

def cmt_buy_market_order(ticker, amount):

    url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
    response = requests.get(url)
    response = response.json()
    # response

    ## List of users in [2] followed by [1] index, spit out a list
    get_users = list(response.items())[2][1]

    num_users = len(get_users)
    print("Number of Users : ", num_users)

    for i in get_users:
        print("User ID : ", i['userid'])
        print("Access Key : ", i['apikey'])
        print("Secret Key : ", i['securitykey'])
        access_key = i['apikey']
        secret_key = i['securitykey']

        upbit = pyupbit.Upbit(access_key, secret_key)  # API 로그인 함수 호출
        upbit #upbit 라는 instance가 생성됨
        KRW_balance = upbit.get_balance()
        print(i['userid'], "Balance : ", KRW_balance)
        upbit.buy_market_order(ticker, amount)
               

    return None


def cmt_sell_market_order(ticker, amount):

    url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
    response = requests.get(url)
    response = response.json()
    # response

    
    ## List of users in [2] followed by [1] index, spit out a list
    get_users = list(response.items())[2][1]

    num_users = len(get_users)
    print("Number of Users : ", num_users)

    for i in get_users:
        print("User ID : ", i['userid'])
        print("Access Key : ", i['apikey'])
        print("Secret Key : ", i['securitykey'])
        access_key = i['apikey']
        secret_key = i['securitykey']

        upbit = pyupbit.Upbit(access_key, secret_key)  # API 로그인 함수 호출
        upbit #upbit 라는 instance가 생성됨
        KRW_balance = upbit.get_balance()
        print(i['userid'], "Balance : ", KRW_balance)
                
        coin_balance = upbit.get_balance(ticker)
        sell_coin = upbit.sell_market_order(ticker, coin_balance) ## Sell all balance

    return None
import requests
import pyupbit

## Buy Function

def buy_market_order(ticker, amount):
    print("Buy Function Activated")
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
        print(i['userid'], "ticker : ", ticker, "Purchased Amount : ", amount)
               

    return None


def sell_market_order(ticker, fraction):
    print("Sell Function Activated")

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
        # KRW_balance = upbit.get_balance()
                        
        coin_balance = upbit.get_balance(ticker)
        print(coin_balance)

        print(i['userid'], "ticker : ", ticker, "ticker Balance : ", coin_balance)

        upbit.sell_market_order(ticker, coin_balance * fraction) ## Sell total_balance * fraction
        # upbit.sell_market_order(ticker, coin_balance) ## Sell total_balance * fraction
        
        coin_balance_updated = upbit.get_balance(ticker)

        print(i['userid'], "ticker : ", ticker, "new ticker Balance : ", coin_balance_updated)

    return None



## Test

print("hello world")
buy_market_order("KRW-ATOM", 5000)
# sell_market_order("KRW-ATOM", 0.5)

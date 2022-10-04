import requests
import pyupbit


## Checking code_status

def code_status():
    import socket  
    is_server = False

    my_IP = socket.gethostbyname(socket.gethostname())
    print("my IP address : ", my_IP)

    server_IP = '121.137.95.97'
    dev_IP = '175.207.155.229'

    if my_IP == server_IP or my_IP == dev_IP:
        print("The code is being run by the server or Jeong's computer")
        is_server = True
    
    else:
        print("The code is being run on a personal computer")

    return is_server


## Buy Function
def buy_market_order(API, ticker, amount):
    ## API = Upbit API instance --> need it to map to the dedicated BOT

    print("Buy Function Activated")    
    is_server = code_status()
    
    ## If the code is being run on a PC, then proceed as normal
    if is_server == False:
        print("is_server is False, hence buy only user's")
        KRW_balance = API.get_balance()
        print("Balance : ", KRW_balance)
        API.buy_market_order_single(ticker, amount) ## This needs separate treatment
        print("ticker : ", ticker, "Purchased Amount : ", amount)

    ## If the code is being run on the server
    else:
        print("is_server is True, hence run through all the users in the server")

        ## This is where we need to map USER to the BOT Name

        ## find the bot that is mapped to the user API.ID
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

            user_upbit = cmt.Upbit(access_key, secret_key)  # Upbit API instance 생성, ID는 무시
            
            KRW_balance = user_upbit.get_balance()
            print(i['userid'], "Balance : ", KRW_balance)
            user_upbit.buy_market_order(ticker, amount)
            print(i['userid'], "ticker : ", ticker, "Purchased Amount : ", amount)
               

    return None


def sell_market_order(ticker, fraction):

    ## API = Upbit API instance --> need it to map to the dedicated BOT

    print("Sell Function Activated")
    is_server = code_status()

        ## If the code is being run on a PC, then proceed as normal
    if is_server == False:
        print("is_server is False, hence buy only user's")
        KRW_balance = API.get_balance()
        print("Balance : ", KRW_balance)
        API.buy_market_order_single(ticker, amount) ## This needs separate treatment
        print("ticker : ", ticker, "Purchased Amount : ", amount)

    ## If the code is being run on the server
    else:
        print("is_server is True, hence run through all the users in the server")

        ## This is where we need to map USER to the BOT Name
        ## find the bot that is mapped to the user API.ID
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

            user_upbit = cmt.Upbit(access_key, secret_key)  # API 로그인 함수 호출
            # KRW_balance = upbit.get_balance()
                            
            coin_balance = user_upbit.get_balance(ticker)
            print(coin_balance)

            print(i['userid'], "ticker : ", ticker, "ticker Balance : ", coin_balance)

            user_upbit.sell_market_order(ticker, coin_balance * fraction) ## Sell total_balance * fraction
            # upbit.sell_market_order(ticker, coin_balance) ## Sell total_balance * fraction
            
            coin_balance_updated = user_upbit.get_balance(ticker)

            print(i['userid'], "ticker : ", ticker, "new ticker Balance : ", coin_balance_updated)

    return None




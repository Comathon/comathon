# -*- coding: utf-8 -*-

"""
comathon.exchange_api

This module provides exchange api of the Upbit API for Comathon Webiste.
"""

import pyupbit
import math
import jwt          # PyJWT
import re
import uuid
import hashlib
import socket
import requests
import time
import datetime as dt
from urllib.parse import urlencode
from pyupbit.request_api import _send_get_request, _send_post_request, _send_delete_request

#
#--------------------------------------------------------------------------
# Comathon Modules
#--------------------------------------------------------------------------
#     

def code_status():
    ## Checks whether the code is being run by the server or by a personal computer
    is_server = False

    my_IP = socket.gethostbyname(socket.gethostname())
    print("my IP address : ", my_IP)


    server_IP = '121.137.95.97'
    server_IP2 = '172.31.58.99'
    aws_IP = '43.201.123.167'
    dev_IP = '175.207.155.229'
    home_IP = '121.142.61.184'
    dev_IP_laptop = '192.168.213.94'
    # dev_IP_school = ''

    if my_IP == server_IP or my_IP == server_IP2 or my_IP == aws_IP or my_IP == dev_IP_laptop or my_IP == dev_IP or my_IP == home_IP:
        print("The code is being run by the server or Jeong's computer")
        is_server = True
    
    else:
        print("The code is being run on a personal computer")
        print("is_server variable : ", is_server)

    return is_server

def server_alive():
    ## Check if the server is online and running
    url = "http://121.137.95.97:8889/Botalive?botid=Bot001"
    response = requests.get(url).json()['ResCode'] 

    if response == "OK":
        server_alive = True        
    else:
        server_alive = False
        
    return server_alive
    


def bot_mapping(userID):
    ## Finds the BOT that the user is mapped to, and returns the BOT address

    ## Bot List
    url = "http://121.137.95.97:8889/BotList"

    response = requests.get(url)
    response = response.json()
    # print(response)

    ## Find the botid that matches my ID
    ## Then create a string url using that botid
    ## Concatenate the bot address, return the very first item
    ## Technically, an user should be mapped to only one bot

    get_bots = list(response.items())[2][1]
    get_bots

    num_bots = len(get_bots)
    # print("Number of active bots : ", num_bots)
    # print("my user ID is :", userID)
    bot_url_list = []

    for i in get_bots:
        save_ID = i['makerid']
        save_botid = i['botid']

        # print(save_ID, save_botid)

        if save_ID == userID:
            bot_connect = save_botid
            # print("the user will be mapped to the bot : ", bot_connect)
            url = "http://121.137.95.97:8889/BotWithinUserList?botid=" + bot_connect
            # print(url)
            bot_url_list.append(url)
        else:
            # print("not this bot")
            pass

    # print(bot_url_list[0])

    return bot_url_list[0] ##Return the first item, as other items are only for test (should be mapped to only one bot)


def get_last_order(API, ticker):
    ## Look for the last order information for a given ticker (both cancel and done)
    ## Compare which one is the latest, return the UUID of the latest order

    order_done = API.get_order(ticker, state="done", limit=1)
    order_cancel = API.get_order(ticker, state="cancel", limit = 1)

    order_done_time = order_done[0]['created_at'][:-6] #Cut out the last 6 digits
    order_cancel_time = order_cancel[0]['created_at'][:-6] #Cut out the last 6 digits

    order_done_time_adjusted = dt.datetime.strptime(order_done_time, '%Y-%m-%dT%H:%M:%S')
    order_cancel_time_adjusted = dt.datetime.strptime(order_cancel_time, '%Y-%m-%dT%H:%M:%S')

    ## Current Time
    c_time = dt.datetime.today()

    ## Get Time Differences
    timediff_done = c_time - order_done_time_adjusted
    timediff_cancel = c_time - order_cancel_time_adjusted

    # print(timediff_done)
    # print(timediff_cancel)

    check = timediff_done < timediff_cancel

    if check == False:
        print("Last Order State = Cancel")
        return order_cancel[0]['uuid']

    else:
        print("Last Order State = Done")
        return order_done[0]['uuid']


def create_order_url(botid, userid, uuid, last_order):

    ## I should pass API which should include  botID, userID

    server = "http://121.137.95.97:8889/" 
    was_item = "botorder" 
    botid = "BOT001"
    userid = "test001"
    uuid = last_order['uuid']
    created_at = last_order['created_at'][:-6].translate({ord(i): None for i in '-T:'}) ##Need to convert the time format to 'YYYYMMDDHHMMSS'
    # created_at = '2022 09 08 11 40 00' #YYYY MM DD HH MM SS
    market = last_order['market']
    side = last_order['side'] ## bid or ask
    volume = last_order['executed_volume']
    price = last_order['trades'][0]['price'] ## ?????????, ????????? ??????
    ord_type = last_order['ord_type'] ## limit, price, market

    if side == 'bid': ## Buy    
        buyprice = last_order['trades'][0]['price'] ## ?????? ??????
        buyvolume = last_order['trades'][0]['volume'] ## ??? ?????????
        buyfee = last_order['paid_fee'] # ???????????????
        order_url = (f'{server}{was_item}?botid={botid}&userid={userid}&uuid={uuid}&created_at={created_at}&market={market}&side={side}&volume={volume}&price={price}&ord_type={ord_type}&buyprice={buyprice}&buyvolume={buyvolume}&buyfee={buyfee}')
        # order_url = (f'{server}{was_item}?botid={botid}&userid={userid}&uuid={uuid}&created_at={created_at}&market={market}&side={side}&volume={volume}&price={price}&ord_type={ord_type}&sellprice={buyprice}&sellvolume={buyvolume}&sellfee={buyfee}')

    elif side == 'ask': ## Sell
        sellprice = last_order['trades'][0]['price'] ## ?????? ??????
        sellvolume = last_order['trades'][0]['volume'] ## ??? ?????????
        sellfee = last_order['paid_fee'] # ???????????????
        # order_url = (f'{server}{was_item}?botid={botid}&userid={userid}&uuid={uuid}&created_at={created_at}&market={market}&side={side}&volume={volume}&price={price}&ord_type={ord_type}&buyprice={buyprice}&buyvolume={buyvolume}&buyfee={buyfee}')
        order_url = (f'{server}{was_item}?botid={botid}&userid={userid}&uuid={uuid}&created_at={created_at}&market={market}&side={side}&volume={volume}&price={price}&ord_type={ord_type}&sellprice={sellprice}&sellvolume={sellvolume}&sellfee={sellfee}')

    return order_url

## Buy Function (CMT Function)
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

        ## find the bot that is mapped to the user API.ID (e.g. test001)
        #@ url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT001"
        url = API.boturl
        response = requests.get(url).json()        
        # response

        ## List of users in [2] followed by [1] index, spit out a list
        get_users = list(response.items())[2][1]

        num_users = len(get_users)
        print("Number of Users : ", num_users)

        for i in get_users:
            print("User ID : ", i['userid'])
            print("Access Key : ", i['apikey'])
            print("Secret Key : ", i['securitykey'])
            user_id = i['userid']
            access_key = i['apikey']
            secret_key = i['securitykey']
            
            user_upbit = pyupbit.Upbit(access_key, secret_key)  # cmt??? ?????? ????????? ??????
            
            KRW_balance = user_upbit.get_balance("KRW")
            print(i['userid'], "Balance : ", KRW_balance)

            user_upbit.buy_market_order(ticker, amount)
            print(i['userid'], "ticker : ", ticker, "Purchased Amount : ", amount)

            try:
                ## Check if the order has been made or not 
                uuid = get_last_order(user_upbit, ticker) ## cmt function, returns uuid
                last_order = user_upbit.get_order(uuid) ##pyupbit function
                # last_order

                ## if yes, then make WAS Request here

                order_url = create_order_url(url[-6:], user_id, uuid, last_order)
                response = requests.get(order_url).json()
                print(response) 

            except:
                print("An exception has occured, probably the purchase was not made")
                continue

            ## if no, then find out why
            

    return print("cmt buy function complete")


## Sell Function (CMT Function)
def sell_market_order(API, ticker, fraction):

    ## API = Upbit API instance --> need it to map to the dedicated BOT

    print("Sell Function Activated")
    is_server = code_status()

        ## If the code is being run on a PC, then proceed as normal
    if is_server == False:
        print("is_server is False, hence buy only user's")
        coin_balance = API.get_balance(ticker)
        print("ticker :", ticker, "ticker Balance : ", coin_balance)
        
        ## coin_balance??? None?????? exception ?????? ??????
        if coin_balance == None:
            print("Coin Balance is None, cannot proceed")
        else:
            print("not this bot")
            API.sell_market_order_single(ticker, coin_balance * fraction) ## This may need separate treatment
            print("ticker : ", ticker, "Sold Amount : ", coin_balance * fraction)

    ## If the code is being run on the server
    else:
        print("is_server is True, hence run through all the users in the server")

        ## This is where we need to map USER to the BOT Name
        ## find the bot that is mapped to the user API.ID
        # url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
        url = API.boturl
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

            user_upbit = pyupbit.Upbit(access_key, secret_key)  # API ????????? ?????? ??????
            # KRW_balance = user_upbit.get_balance()
                            
            coin_balance = user_upbit.get_balance(ticker)
            print(i['userid'], "ticker : ", ticker, "ticker Balance : ", coin_balance)
            if coin_balance == None:
                print("Coin Balance is None, cannot proceed")
            else:
                ## coin_balance??? None?????? exception ?????? ??????
                user_upbit.sell_market_order(ticker, coin_balance * fraction) ## Sell total_balance * fraction
                # upbit.sell_market_order(ticker, coin_balance) ## Sell total_balance * fraction
                
                coin_balance_updated = user_upbit.get_balance(ticker)

                print(i['userid'], "ticker : ", ticker, "new ticker Balance : ", coin_balance_updated)

                ## Make WAS Request here

    return print("cmt sell function complete")


#
#--------------------------------------------------------------------------
# Original Pyupbit Module
#--------------------------------------------------------------------------
#     

def get_tick_size(price, method="floor"):
    """???????????? ?????? ?????? ?????? 

    Args:
        price (float]): ?????? ?????? 
        method (str, optional): ?????? ?????? ?????? ??????. Defaults to "floor".

    Returns:
        float: ????????? ?????? ?????? ?????? ?????? ????????? ????????? ?????? 
    """

    if method == "floor":
        func = math.floor
    elif method == "round":
        func = round 
    else:
        func = math.ceil 

    if price >= 2000000:
        tick_size = func(price / 1000) * 1000
    elif price >= 1000000:
        tick_size = func(price / 500) * 500
    elif price >= 500000:
        tick_size = func(price / 100) * 100
    elif price >= 100000:
        tick_size = func(price / 50) * 50
    elif price >= 10000:
        tick_size = func(price / 10) * 10
    elif price >= 1000:
        tick_size = func(price / 5) * 5
    elif price >= 100:
        tick_size = func(price / 1) * 1
    elif price >= 10:
        tick_size = func(price / 0.1) / 10
    elif price >= 1:
        tick_size = func(price / 0.01) / 100
    elif price >= 0.1:
        tick_size = func(price / 0.001) / 1000
    else:
        tick_size = func(price / 0.0001) / 10000

    return tick_size


#
#--------------------------------------------------------------------------
# CMT UpbitAPI Class
#--------------------------------------------------------------------------
#     


class Upbit:
    def __init__(self, access, secret, cmt_ID=None):
        self.access = access
        self.secret = secret
        self.userID = cmt_ID
        
        if cmt_ID == None:
            print("**------- Note : No CMT_ID given, CMT_Upbit Instance is not mapped to any BOT ------- **")
            self.botID = None
            self.boturl = None
            pass
        else:
            self.botID = bot_mapping(self.userID)[-6:]
            self.boturl = bot_mapping(self.userID)
            print("User's Comathon Account : ", self.userID, ", is now mapped to :", self.botID)

        code_status()
        
        ## must continuously update the num_investors  


    def _request_headers(self, query=None):
        payload = {
            "access_key": self.access,
            "nonce": str(uuid.uuid4())
        }

        if query is not None:
            m = hashlib.sha512()
            m.update(urlencode(query, doseq=True).replace("%5B%5D=", "[]=").encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        #jwt_token = jwt.encode(payload, self.secret, algorithm="HS256").decode('utf-8')
        jwt_token = jwt.encode(payload, self.secret, algorithm="HS256")     # PyJWT >= 2.0
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}
        return headers


    #--------------------------------------------------------------------------
    # ?????? 
    #--------------------------------------------------------------------------
    #     ?????? ?????? ??????
    def get_balances(self, contain_req=False):
        """
        ?????? ?????? ??????
        :param contain_req: Remaining-Req ????????????
        :return: ?????? ????????? ?????? ?????????
        [contain_req == True ??? ?????? Remaining-Req??? ??????]
        """
        url = "https://api.upbit.com/v1/accounts"
        headers = self._request_headers()
        result = _send_get_request(url, headers=headers)
        if contain_req:
            return result
        else:
            return result[0]


    def get_balance(self, ticker="KRW", verbose=False, contain_req=False):
        """
        ?????? ??????/????????? ????????? ???????????? ?????????
        :param ticker: ????????? ???????????? ?????? ????????? ??????
        :param verbose: False: only the balance, True: original dictionary 
        :param contain_req: Remaining-Req ????????????
        :return: ???????????? ??????/?????? (?????? ??? ???????????? ??????/?????? ??????)
        [contain_req == True ??? ?????? Remaining-Req??? ??????]
        """
        try:
            # fiat-ticker
            # KRW-BTC
            fiat = "KRW"
            if '-' in ticker:
                fiat, ticker = ticker.split('-')

            balances, req = self.get_balances(contain_req=True)

            # search the current currency
            balance = 0
            for x in balances:
                if x['currency'] == ticker and x['unit_currency'] == fiat:
                    if verbose is True:
                        balance = x 
                    else:
                        balance = float(x['balance'])
                    break

            if contain_req:
                return balance, req
            else:
                return balance
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_balance_t(self, ticker='KRW', contain_req=False):
        """
        ?????? ??????/????????? ?????? ??????(balance + locked)
        :param ticker: ????????? ???????????? ?????? ????????? ??????
        :param contain_req: Remaining-Req ????????????
        :return: ???????????? ??????/?????? (?????? ??? ???????????? ??????/?????? ??????)
        [contain_req == True ??? ?????? Remaining-Req??? ??????]
        """
        try:
            # KRW-BTC
            if '-' in ticker:
                ticker = ticker.split('-')[1]

            balances, req = self.get_balances(contain_req=True)

            balance = 0
            locked = 0
            for x in balances:
                if x['currency'] == ticker:
                    balance = float(x['balance'])
                    locked = float(x['locked'])
                    break

            if contain_req:
                return balance + locked, req
            else:
                return balance + locked
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_avg_buy_price(self, ticker='KRW', contain_req=False):
        """
        ?????? ??????/????????? ??????????????? ??????
        :param ticker: ????????? ???????????? ?????? ????????? ??????
        :param contain_req: Remaining-Req ????????????
        :return: ???????????????
        [contain_req == True ??? ?????? Remaining-Req??? ??????]
        """
        try:
            # KRW-BTC
            if '-' in ticker:
                ticker = ticker.split('-')[1]

            balances, req = self.get_balances(contain_req=True)

            avg_buy_price = 0
            for x in balances:
                if x['currency'] == ticker:
                    avg_buy_price = float(x['avg_buy_price'])
                    break
            if contain_req:
                return avg_buy_price, req
            else:
                return avg_buy_price

        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_amount(self, ticker, contain_req=False):
        """
        ?????? ??????/????????? ???????????? ??????
        :param ticker: ????????? ???????????? ?????? ????????? ?????? (ALL ????????? ??? ???????????? ??????)
        :param contain_req: Remaining-Req ????????????
        :return: ????????????
        [contain_req == True ??? ?????? Remaining-Req??? ??????]
        """
        try:
            # KRW-BTC
            if '-' in ticker:
                ticker = ticker.split('-')[1]

            balances, req = self.get_balances(contain_req=True)

            amount = 0
            for x in balances:
                if x['currency'] == 'KRW':
                    continue

                avg_buy_price = float(x['avg_buy_price'])
                balance = float(x['balance'])
                locked = float(x['locked'])

                if ticker == 'ALL':
                    amount += avg_buy_price * (balance + locked)
                elif x['currency'] == ticker:
                    amount = avg_buy_price * (balance + locked)
                    break
            if contain_req:
                return amount, req
            else:
                return amount
        except Exception as x:
            print(x.__class__.__name__)
            return None

    ## endregion balance


    #--------------------------------------------------------------------------
    # ?????? 
    #--------------------------------------------------------------------------
    #     ?????? ?????? ??????
    def get_chance(self, ticker, contain_req=False):
        """
        ????????? ?????? ?????? ????????? ??????.
        :param ticker:
        :param contain_req: Remaining-Req ????????????
        :return: ????????? ?????? ?????? ????????? ??????
        [contain_req == True ??? ?????? Remaining-Req??? ??????]
        """
        try:
            url = "https://api.upbit.com/v1/orders/chance"
            data = {"market": ticker}
            headers = self._request_headers(data)
            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None
    

    #    ?????? ?????? ?????? 
    def get_order(self, ticker_or_uuid, state='wait', page=1, limit=100, contain_req=False):
        """
        ?????? ????????? ??????
        :param ticker: market
        :param state: ?????? ??????(wait, watch, done, cancel)
        :param kind: ?????? ??????(normal, watch)
        :param contain_req: Remaining-Req ????????????
        :return:
        """
        # TODO : states, identifiers ?????? ?????? ?????? ??????
        try:
            p = re.compile(r"^\w+-\w+-\w+-\w+-\w+$")
            # ???????????? ????????? ???????????? ?????? ??? ?????? ???????????? ???????????? ???
            # - r"^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$"
            is_uuid = len(p.findall(ticker_or_uuid)) > 0
            if is_uuid:
                url = "https://api.upbit.com/v1/order"
                data = {'uuid': ticker_or_uuid}
                headers = self._request_headers(data)
                result = _send_get_request(url, headers=headers, data=data)
            else :

                url = "https://api.upbit.com/v1/orders"
                data = {'market': ticker_or_uuid,
                        'state': state,
                        'page': page,
                        'limit': limit,
                        'order_by': 'desc'
                        }
                headers = self._request_headers(data)
                result = _send_get_request(url, headers=headers, data=data)

            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    def get_individual_order(self, uuid, contain_req=False):
        """
        ?????? ????????? ??????
        :param uuid: ?????? id
        :param contain_req: Remaining-Req ????????????
        :return:
        """
        # TODO : states, uuids, identifiers ?????? ?????? ?????? ??????
        try:
            url = "https://api.upbit.com/v1/order"
            data = {'uuid': uuid}
            headers = self._request_headers(data)
            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    #    ?????? ?????? ??????
    def cancel_order(self, uuid, contain_req=False):
        """
        ?????? ??????
        :param uuid: ?????? ????????? ?????? ?????? uuid
        :param contain_req: Remaining-Req ????????????
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/order"
            data = {"uuid": uuid}
            headers = self._request_headers(data)
            result = _send_delete_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #     ?????? 
    def buy_limit_order_single(self, ticker, price, volume, contain_req=False):
        """
        ????????? ??????
        :param ticker: ?????? ??????
        :param price: ?????? ??????
        :param volume: ?????? ??????
        :param contain_req: Remaining-Req ????????????
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "bid",
                    "volume": str(volume),
                    "price": str(price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    ## Buy Function (CMT Function)
    def buy_market_order(self, ticker, amount):
        ## API = Upbit API instance --> need it to map to the dedicated BOT

        print("Buy Function Activated")    
        is_server = code_status()
        
        ## If the code is being run on a PC, then proceed as normal
        if is_server == False:
            print("is_server is False, hence buy only user's")
            KRW_balance = self.get_balance()
            print("Balance : ", KRW_balance)
            self.buy_market_order_single(ticker, amount) ## This needs separate treatment
            print("ticker : ", ticker, "Purchased Amount : ", amount)

        ## If the code is being run on the server
        else:
            print("is_server is True, hence run through all the users in the server")
            ## This is where we need to map USER to the BOT Name

            ## find the bot that is mapped to the user API.ID
            # url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
            url = API.boturl
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

                user_upbit = pyupbit.Upbit(access_key, secret_key)  # cmt??? ?????? ????????? ??????
                
                KRW_balance = user_upbit.get_balance("KRW")
                print(i['userid'], "Balance : ", KRW_balance)

                user_upbit.buy_market_order(ticker, amount)
                print(i['userid'], "ticker : ", ticker, "Purchased Amount : ", amount)
                

        return None


    def sell_market_order(self, ticker, fraction):

        ## API = Upbit API instance --> need it to map to the dedicated BOT

        print("Sell Function Activated")
        is_server = code_status()

            ## If the code is being run on a PC, then proceed as normal
        if is_server == False:
            print("is_server is False, hence buy only user's")
            coin_balance = self.get_balance(ticker)
            print("ticker :", ticker, "ticker Balance : ", coin_balance)
            
            ## coin_balance??? None?????? exception ?????? ??????
            if coin_balance == None:
                print("Coin Balance is None, cannot proceed")
            else:
                self.sell_market_order_single(ticker, coin_balance * fraction) ## This may need separate treatment
                print("ticker : ", ticker, "Sold Amount : ", coin_balance * fraction)

        ## If the code is being run on the server
        else:
            print("is_server is True, hence run through all the users in the server")

            ## This is where we need to map USER to the BOT Name
            ## find the bot that is mapped to the user API.ID
            # url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
            url = API.boturl
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

                user_upbit = pyupbit.Upbit(access_key, secret_key)  # API ????????? ?????? ??????
                # KRW_balance = user_upbit.get_balance()
                                
                coin_balance = user_upbit.get_balance(ticker)
                print(i['userid'], "ticker : ", ticker, "ticker Balance : ", coin_balance)
                if coin_balance == None:
                    print("Coin Balance is None, cannot proceed")
                else:
                    ## coin_balance??? None?????? exception ?????? ??????
                    user_upbit.sell_market_order(ticker, coin_balance * fraction) ## Sell total_balance * fraction
                    # upbit.sell_market_order(ticker, coin_balance) ## Sell total_balance * fraction
                    
                    coin_balance_updated = user_upbit.get_balance(ticker)

                    print(i['userid'], "ticker : ", ticker, "new ticker Balance : ", coin_balance_updated)


        return None

    def buy_market_order_single(self, ticker, price, contain_req=False):
        """
        ????????? ??????
        :param ticker: ticker for cryptocurrency
        :param price: KRW
        :param contain_req: Remaining-Req ????????????
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,  # market ID
                    "side": "bid",  # buy
                    "price": str(price),
                    "ord_type": "price"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def sell_market_order_single(self, ticker, volume, contain_req=False):
        """
        ????????? ?????? ?????????
        :param ticker: ???????????? ??????
        :param volume: ??????
        :param contain_req: Remaining-Req ????????????
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,  # ticker
                    "side": "ask",  # sell
                    "volume": str(volume),
                    "ord_type": "market"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def sell_limit_order_single(self, ticker, price, volume, contain_req=False):
        """
        ????????? ??????
        :param ticker: ?????? ??????
        :param price: ?????? ??????
        :param volume: ?????? ??????
        :param contain_req: Remaining-Req ????????????
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "ask",
                    "volume": str(volume),
                    "price": str(price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #--------------------------------------------------------------------------
    # ??????
    #--------------------------------------------------------------------------
    # def get_withdraw_list(self, currency: str, contain_req=False):
    #     """
    #     ?????? ????????? ??????
    #     :param currency: Currency ??????
    #     :param contain_req: Remaining-Req ????????????
    #     :return:
    #     """
    #     try:
    #         url = "https://api.upbit.com/v1/withdraws"
    #         data = {"currency": currency}
    #         headers = self._request_headers(data)

    #         result = _send_get_request(url, headers=headers, data=data)
    #         if contain_req:
    #             return result
    #         else:
    #             return result[0]
    #     except Exception as x:
    #         print(x.__class__.__name__)
    #         return None

    # #     ?????? ?????? ??????
    # def get_individual_withdraw_order(self, uuid: str, currency: str, contain_req=False):
    #     """
    #     ?????? ?????? ??????
    #     :param uuid: ?????? UUID
    #     :param currency: Currency ??????
    #     :param contain_req: Remaining-Req ????????????
    #     :return:
    #     """
    #     try:
    #         url = "https://api.upbit.com/v1/withdraw"
    #         data = {"uuid": uuid, "currency": currency}
    #         headers = self._request_headers(data)
    #         result = _send_get_request(url, headers=headers, data=data)
    #         if contain_req:
    #             return result
    #         else:
    #             return result[0]
    #     except Exception as x:
    #         print(x.__class__.__name__)
    #         return None


    # #     ?????? ????????????  
    # def withdraw_coin(self, currency, amount, address, secondary_address='None', transaction_type='default', contain_req=False):
    #     """
    #     ?????? ??????
    #     :param currency: Currency symbol
    #     :param amount: ?????? ??????
    #     :param address: ?????? ?????? ??????
    #     :param secondary_address: 2??? ???????????? (????????? ????????? ?????????)
    #     :param transaction_type: ?????? ??????
    #     :param contain_req: Remaining-Req ????????????
    #     :return:
    #     """
    #     try:
    #         url = "https://api.upbit.com/v1/withdraws/coin"
    #         data = {"currency": currency,
    #                 "amount": amount,
    #                 "address": address,
    #                 "secondary_address": secondary_address,
    #                 "transaction_type": transaction_type}
    #         headers = self._request_headers(data)
    #         result = _send_post_request(url, headers=headers, data=data)
    #         if contain_req:
    #             return result
    #         else:
    #             return result[0]
    #     except Exception as x:
    #         print(x.__class__.__name__)
    #         return None


    # #     ?????? ????????????
    # def withdraw_cash(self, amount: str, contain_req=False):
    #     """
    #     ?????? ??????
    #     :param amount: ?????? ??????
    #     :param contain_req: Remaining-Req ????????????
    #     :return:
    #     """
    #     try:
    #         url = "https://api.upbit.com/v1/withdraws/krw"
    #         data = {"amount": amount}
    #         headers = self._request_headers(data)
    #         result = _send_post_request(url, headers=headers, data=data)
    #         if contain_req:
    #             return result
    #         else:
    #             return result[0]
    #     except Exception as x:
    #         print(x.__class__.__name__)
    #         return None


    #--------------------------------------------------------------------------
    # ?????? 
    #--------------------------------------------------------------------------
    #     ?????? ????????? ?????? 
    # def get_deposit_list(self, currency: str, contain_req=False):
    #     """
    #     ?????? ????????? ??????
    #     :currency: Currency ??????
    #     :param contain_req: Remaining-Req ????????????
    #     :return:
    #     """
    #     try:
    #         url = "https://api.upbit.com//v1/deposits"
    #         data = {"currency": currency}
    #         headers = self._request_headers(data)

    #         result = _send_get_request(url, headers=headers, data=data)
    #         if contain_req:
    #             return result
    #         else:
    #             return result[0]
    #     except Exception as x:
    #         print(x.__class__.__name__)
    #         return None
            
    # #     ?????? ?????? ??????
    # def get_individual_deposit_order(self, uuid: str, currency: str, contain_req=False):
    #     """
    #     ?????? ?????? ??????
    #     :param uuid: ?????? UUID
    #     :param currency: Currency ??????
    #     :param contain_req: Remaining-Req ????????????
    #     :return:
    #     """
    #     try:
    #         url = "https://api.upbit.com/v1/deposit"
    #         data = {"uuid": uuid, "currency": currency}
    #         headers = self._request_headers(data)
    #         result = _send_get_request(url, headers=headers, data=data)
    #         if contain_req:
    #             return result
    #         else:
    #             return result[0]
    #     except Exception as x:
    #         print(x.__class__.__name__)
    #         return None


    #     ?????? ?????? ?????? ?????? 
    #     ?????? ?????? ?????? ??????
    #     ?????? ?????? ?????? ??????
    #     ?????? ????????????


    #--------------------------------------------------------------------------
    # ????????? ?????? 
    #--------------------------------------------------------------------------
    #     ????????? ?????? 
    # def get_deposit_withdraw_status(self, contain_req=False):
    #     url = "https://api.upbit.com/v1/status/wallet"
    #     headers = self._request_headers()
    #     result = _send_get_request(url, headers=headers)
    #     if contain_req:
    #         return result
    #     else:
    #         return result[0]


    # #     API??? ????????? ??????
    # def get_api_key_list(self, contain_req=False):
    #     url = "https://api.upbit.com/v1/api_keys"
    #     headers = self._request_headers()
    #     result = _send_get_request(url, headers=headers)
    #     if contain_req:
    #         return result
    #     else:
    #         return result[0]


# if __name__ == "__main__":
#     import pprint

#     #-------------------------------------------------------------------------
#     # api key
#     #-------------------------------------------------------------------------
#     with open("../upbit.key") as f:
#         lines = f.readlines()
#         access = lines[0].strip()
#         secret = lines[1].strip()

#     upbit = Upbit(access, secret)
#     #print(upbit.get_balances())
#     print(upbit.get_balance("KRW-BTC", verbose=True))

#     # order 
#     resp = upbit.buy_limit_order("KRW-XRP", 500, 10)
#     print(resp)


    #-------------------------------------------------------------------------
    # ?????? 
    #     ?????? ?????? ?????? 
    #balance = upbit.get_balances()
    #pprint.pprint(balance)

    #balances = upbit.get_order("KRW-XRP")
    #pprint.pprint(balances)

    # order = upbit.get_order('50e184b3-9b4f-4bb0-9c03-30318e3ff10a')
    # print(order)
    # # ?????? ?????? ??????
    # print(upbit.get_balance(ticker="KRW"))          # ?????? KRW
    # print(upbit.get_amount('ALL'))                  # ???????????????
    # print(upbit.get_balance(ticker="KRW-BTC"))      # ???????????? ????????????
    # print(upbit.get_balance(ticker="KRW-XRP"))      # ?????? ????????????

    #-------------------------------------------------------------------------
    # ??????
    #     ?????? ?????? ?????? 
    #pprint.pprint(upbit.get_chance('KRW-BTC'))

    #     ?????? ?????? ??????
    #print(upbit.get_order('KRW-BTC'))

    # ??????
    # print(upbit.sell_limit_order("KRW-XRP", 1000, 20))

    # ??????
    # print(upbit.buy_limit_order("KRW-XRP", 200, 20))

    # ?????? ??????
    # print(upbit.cancel_order('82e211da-21f6-4355-9d76-83e7248e2c0c'))

    # ????????? ?????? ?????????
    # upbit.buy_market_order("KRW-XRP", 10000)

    # ????????? ?????? ?????????
    # upbit.sell_market_order("KRW-XRP", 36)


    #-------------------------------------------------------------------------
    # ????????? ??????
    #     ????????? ??????
    #resp = upbit.get_deposit_withdraw_status()
    #pprint.pprint(resp)

    #     API??? ????????? ??????
    #resp = upbit.get_api_key_list()
    #print(resp)
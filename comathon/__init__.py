# import requests

# from .cmt_test_obsolete import *
from .cmt_exchange import *
from .cmt_quotation import *
import socket

print("Comathon Update 2022 12 25 10:39, BOT_MAPPING Modified")
print("Comathon Module Imported, GAZUA")

## Check if the code is being run from the server of from the personal computer

## Create API upbit instances here? Then how can we check if someone cut out the connection or added a one?

def code_status():
    ## Checks whether the code is being run by the server or by a personal computer
    is_server = False

    my_IP = socket.gethostbyname(socket.gethostname())
    print("my IP address : ", my_IP)

    server_IP = '121.137.95.97'
    aws_IP = '43.201.123.167'
    dev_IP = '175.207.155.229'
    home_IP = '121.142.61.184'
    dev_IP_laptop = '192.168.213.94'
    # dev_IP_school = ''

    if my_IP == server_IP or my_IP == aws_IP or my_IP == dev_IP_laptop or my_IP == dev_IP or my_IP == home_IP:
        print("The code is being run by the server or Jeong's computer")
        is_server = True
    
    else:
        print("The code is being run on a personal computer")
        print("is_server variable : ", is_server)

    return is_server

code_status()



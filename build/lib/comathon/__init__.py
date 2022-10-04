# import requests

from .cmt_test import *
from .cmt_exchange import *
from .cmt_quotation import *
import socket

print("Comathon Module Imported, GAZUA")

## Check if the code is being run from the server of from the personal computer

## Create API upbit instances here? Then how can we check if someone cut out the connection or added a one?


import socket  

my_IP = socket.gethostbyname(socket.gethostname())

server_IP = '121.137.95.97'
dev_IP = '175.207.155.229'

if my_IP == server_IP or my_IP == dev_IP:
    print("The code is being run by the server or Jeong's computer")

else:
    print("The code is being run on a personal computer")





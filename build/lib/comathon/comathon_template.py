import comathon as cmt
import requests


## Create UPBIT API Class Instance (업로드 시 삭제)------------------

access_key = "DplIC0dHKeVVjr9RtRhJskZD2xVTkxdQtHno6BpO"
secret_key = "6xV4OlFjLv7P8PoHyuOrRgE1Qk1kmnEfB8Mmzmh4"
comathon_ID = "kptib88"

# myAPI = cmt.Upbit(access_key, secret_key)  # API 로그인 함수 호출
# myAPI #myAPI 라는 instance가 생성됨

myAPI = cmt.Upbit(access_key, secret_key, comathon_ID)  # API 로그인 함수 호출
myAPI #myAPI 라는 instance가 생성됨
myAPI.get_balance("KRW")
##-------------------------------------------------------------------



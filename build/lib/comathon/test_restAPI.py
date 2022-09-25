import requests

print("Hello World")

print("Get Bot List")

url = "http://121.137.95.97:8889/BotList"
response = requests.get(url)
print(response.json())

print("Call Bot 001")

url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT001"
response = requests.get(url)
print(response.json())


print("Call Bot 002")

url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
response = requests.get(url)
print(response.json())

print("End")


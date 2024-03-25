import requests
import time
import json

print("1. БЕЗ GET-параметра токен. Создание задачи:")
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print("Статус код:", response.status_code)
print("Ответ сервера:", response.text)
print()

data = response.json()
token = data['token']
seconds = data['seconds']

print("2. С Неверным GET-параметром токен. ERROR :")
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": "error"})
print("Статус код:", response.status_code)
print("Ответ сервера:", response.text)
print()

print("3. С GET-параметром токен. Решение задачи без таймера:")
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": {token}})
print("Статус код:", response.status_code)
print("Ответ сервера:", response.text)
print()

print("4. С GET-параметром токен. Решение задачи с таймером:")
time.sleep(seconds)
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": {token}})
print("Статус код:", response.status_code)
print("Ответ сервера:", response.text)
print()

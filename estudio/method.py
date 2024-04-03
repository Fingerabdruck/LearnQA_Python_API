import requests

print("1. HTTP-запрос без параметра method:")
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Статус код:", response.status_code)
print("Ответ сервера:", response.text)
print()

print("2. HTTP-запрос не из списка. Например HEAD:")
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Статус код:", response.status_code)
print("Ответ сервера:", response.text)
print()

print("3. HTTP-запрос с правильным значением method:")
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
print("Статус код:", response.status_code)
print("Ответ сервера:", response.text)
print()

print("4. Проверка всех методов:")

http_methods = ["GET", "POST", "PUT", "DELETE"]

for method in http_methods:
    for param_method in http_methods:
        if method == "GET":
            response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": param_method})
        else:
            response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": param_method})

        if response.status_code == 200:
            print(f"Реальный тип запроса: {method}, Значение параметра method: {param_method}")
            print("Ответ сервера:", response.text)
            print("Статус код:", response.status_code)
            print()

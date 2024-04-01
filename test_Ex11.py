import requests
import pytest
class TestEx11:
    def test_Ex11(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print("Status Code:", response.status_code)
        print("Cookies:", response.cookies)
        print()
        assert response.cookies is not None

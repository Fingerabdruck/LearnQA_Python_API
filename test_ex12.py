import requests
import pytest
class TestEx12:
    def test_ex12(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print()
        assert response.headers is not None

import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import json

class TestUserGet(BaseCase):
    def test_user_get_info_no_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'lastName')
        Assertions.assert_json_has_not_key(response, 'firstName')

    def test_user_get_with_auth(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        Assertions.assert_code_status(response1, 200)


        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id_from_auth_method}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_user_get_with_auth_invalid_id(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        Assertions.assert_code_status(response3, 200)

        self.auth_sid = self.get_cookie(response3, "auth_sid")
        self.token = self.get_header(response3, "x-csrf-token")

        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/1",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_json_has_key(response4, 'username')
        Assertions.assert_json_has_not_key(response4, 'email')
        Assertions.assert_json_has_not_key(response4, 'lastName')
        Assertions.assert_json_has_not_key(response4, 'firstName')

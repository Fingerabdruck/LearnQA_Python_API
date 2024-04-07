import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import json

class TestUserRegister(BaseCase):
    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"
        self.email_error = f"{base_part}{random_part}{domain}"
        self.empty_field = [
            {'password': '', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa',
             'email': self.email},
            {'password': '123', 'username': '', 'firstName': 'learnqa', 'lastName': 'learnqa',
             'email': self.email},
            {'password': '123', 'username': 'learnqa', 'firstName': '', 'lastName': 'learnqa',
             'email': self.email},
            {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': '',
             'email': self.email},
            {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa',
             'email': ''}
        ]

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        existing_email = 'vinkotov@example.com'
        user_data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': existing_email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=user_data)
        Assertions.assert_code_status(response, 400)
        print(response.content)
        assert response.content.decode("utf-8") == f"Users with email '{existing_email}' already exists", f"Unexpected response content {response.content.decode('utf-8')}"

    def test_create_user_without_dog(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email_error
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

#ПРОСЬБА ТЕСТЫ НИЖЕ ПРОВЕРИТЬ, У МЕНЯ ПОСТОЯННО ВЫДАЕТ ОШИБКУ, КОД РЕВЬЮ ЧЕРЕЗ ЧАТ ЖПТ НЕ ПОКАЗЫВАЕТ НИЧЕГО
    @pytest.mark.parametrize("test_data", self.empty_field)
    def test_create_user_empty_field(self, test_data):
        response = requests.post('https://playground.learnqa.ru/api/user/', data=test_data)
        print(response.content)

    def test_create_user_name_is_small(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'A',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 400)
        print(response.content)

    def test_create_user_name_is_long(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'A' * 251,
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 400)
        print(response.content)
        
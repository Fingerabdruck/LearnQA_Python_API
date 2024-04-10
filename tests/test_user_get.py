from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
@allure.epic("Get info users")
class TestUserGet(BaseCase):
    @allure.description("Get info user no auth")
    def test_user_get_info_no_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'lastName')
        Assertions.assert_json_has_not_key(response, 'firstName')

    @allure.description("Get info user with auth")
    def test_user_get_with_auth(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)


        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{self.user_id_from_auth_method}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("Get info user with auth invalid id")
    def test_user_get_with_auth_invalid_id(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response3 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response3, 200)

        self.auth_sid = self.get_cookie(response3, "auth_sid")
        self.token = self.get_header(response3, "x-csrf-token")

        response4 = MyRequests.get(
            f"/user/1",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_json_has_key(response4, 'username')
        Assertions.assert_json_has_not_key(response4, 'email')
        Assertions.assert_json_has_not_key(response4, 'lastName')
        Assertions.assert_json_has_not_key(response4, 'firstName')

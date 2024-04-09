from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class TestUserEditNegative(BaseCase):
    def test_user_edit_negative(self):
        # REGISTER - - Попытаемся изменить данные пользователя, будучи неавторизованными
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN - - Попытаемся изменить данные пользователя, будучи неавторизованными
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT - - Попытаемся изменить данные пользователя, будучи неавторизованными
        new_name = "Change Name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response3, 400)

        # LOGIN2 - - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
        login_data2 = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response4 = MyRequests.post("/user/login", data=login_data2)

        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")

        # EDIT2 - - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
        new_name = "Change Name"
        response5 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token2},
                                 cookies={"auth_sid": auth_sid2},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response5, 400)



        # EDIT3 EMAIL - Попытаемся изменить email пользователя,
        # будучи авторизованными тем же пользователем, на новый email без символа @

        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email_error = f"{base_part}{random_part}{domain}"
        response6 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": email_error}
                                 )
        Assertions.assert_code_status(response6, 400)


        # EDIT 3 - - Попытаемся изменить firstName пользователя,
        # будучи авторизованными тем же пользователем, на очень короткое значение в один символ

        new_name3 = "C"
        response7 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name3}
                                 )
        Assertions.assert_code_status(response7, 400)

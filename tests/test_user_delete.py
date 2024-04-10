from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.description("Create user, authorization and delete, check")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("New", "Essentials", "Authentication")
    @allure.testcase("TMS-456")
    def test_user_delete(self):
    # REGISTER NEW - Создать пользователя, авторизоваться из-под него, удалить,
    # затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        Assertions.assert_code_status(response1, 200), f"Упал первый запрос"

    # LOGIN - Создать пользователя, авторизоваться из-под него, удалить,
    # затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        Assertions.assert_code_status(response2, 200), f"упал второй запрос"

    # DELETE USER POSITIVE - Создать пользователя, авторизоваться из-под него, удалить,
    # затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.

        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      )

        Assertions.assert_code_status(response3, 200), f"упал третий запрос"

    # CHECK DELETE USER
        response4 = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_code_status(response3, 200), f"упал упал четвертый запрос"
        assert response4.content.decode("utf-8") == f"User not found"

    #LOGIN ID 2 -  на попытку удалить пользователя по ID 2.
    @allure.description("Delete user id 2")
    def test_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response5 = MyRequests.post("/user/login", data=data)

        self.auth_sid2 = self.get_cookie(response5, "auth_sid")
        self.token2 = self.get_header(response5, "x-csrf-token")

        response6 = MyRequests.delete("/user/2",
                                      headers={"x-csrf-token": self.token2},
                                      cookies={"auth_sid": self.auth_sid2},
                                      )

        Assertions.assert_code_status(response6, 400), f"упал третий запрос"
        assert response6.content.decode("utf-8") == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}'


    # негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
        response7 = MyRequests.delete("/user/2",
                                      headers=None,
                                      cookies=None)
        Assertions.assert_code_status(response7, 400)
        assert response7.content.decode("utf-8") == '{"error":"Auth token not supplied"}'

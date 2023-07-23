from pages.registration.login_page import LoginPage
from utilities.check_status import CheckStatus
from utilities.util import Util
import pytest
import allure
from utilities.read_csv import read_data as rd

# Run specific suite test cases from different files
#  py.test -m smoke registration/*_tests.py --browser chrome

"""
Allure Reports
pip3 install allure-pytest
Mac: py.test -m smoke registration/*_tests.py --browser chrome --alluredir="/Users/aniltomar/PycharmProjects/SeleniumPythonProjectMay2023/reports"
Windows: py.test -m smoke registration/*_tests.py --browser chrome --alluredir="C:\\projectpath\\reports"
allure serve "/Users/aniltomar/PycharmProjects/SeleniumPythonProjectMay2023/reports"
"""


@pytest.mark.usefixtures("setup_teardown_class")
@allure.severity(allure.severity_level.TRIVIAL)
@allure.feature("Login Feature")
class TestLogin():

    @classmethod
    def setup_class(cls):
        cls.lp = LoginPage(cls.driver)
        cls.ut = Util()
        cls.lp.navigate_to_login()
        cls.cs = CheckStatus(cls.driver)

    @pytest.mark.parametrize("username, password", [
        ("testing1@email.com", "password1"),
        ("testing2email.com", "password1"),
        ("@testing3emailcom", "password1")
    ])
    # @pytest.mark.parametrize("username, password", rd("login_test_data.csv"))
    @pytest.mark.sanity
    def test_invalid_username(self, username, password):
        self.lp.login(username, password)
        result = self.lp.verify_invalid_username_error_message()
        self.cs.mark_result(result, "Invalid username error message verification")
        # assert not result

    @pytest.mark.smoke
    @allure.story("User story for empty username")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_empty_username(self):
        self.lp.refresh()
        allure.step("Refresh the browser window")
        self.lp.login("", "")
        allure.step("Try to login with empty username")
        result = self.lp.verify_empty_username_error_message()
        # if not result:
        #     self.lp.take_screenshot()
        # assert result
        self.cs.mark_result(result, "Empty username error message verification")
        title_result = self.lp.verify_title("Login")
        self.cs.mark_result(title_result, "Page title verification")


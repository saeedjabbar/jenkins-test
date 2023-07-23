import time

from pages.registration.login_page import LoginPage
from utilities.check_status import CheckStatus
from utilities.util import Util
import pytest
from utilities.read_csv import read_data as rd
import allure


@pytest.mark.usefixtures("setup_teardown_class")
@allure.feature("Home Page Feature")
class TestLogin():

    @classmethod
    def setup_class(cls):
        cls.lp = LoginPage(cls.driver)
        cls.ut = Util()
        cls.cs = CheckStatus(cls.driver)

    @pytest.mark.sanity
    def test_home1(self):
        self.cs.mark_result(True, "Make the verification successful")

    @pytest.mark.smoke
    @allure.story("User story for home page")
    @allure.severity(allure.severity_level.MINOR)
    def test_home2(self):
        self.cs.mark_result(False, "Make the verification fail")

import time
from base.base_page import BasePage
from utilities.util import Util


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.ut = Util()

    # Locators
    _sign_in_link = "//a[normalize-space()='Sign In']"
    _email_field = "email"
    _password_field = "login-password"
    _login_button = "login"
    _invalid_username_error_message = "//span[@class='dynamic-text help-block']"
    _empty_username_error_message = "//span[@class='error']"

    def navigate_to_login(self):
        self.get_element("xpath", self._sign_in_link).click()
        # self.log("Clicked on sign in button")

    def enter_email(self, email):
        # self.get_element("id", self._email_field).send_keys(email)
        self.send_keys_when_ready(email, "id", self._email_field)

    def enter_password(self, password):
        # self.get_element("id", self._password_field).send_keys(password)
        self.send_keys_when_ready(password, "id", self._password_field)

    def click_login_button(self):
        time.sleep(1)
        self.click_element_when_ready("id", self._login_button)

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def verify_invalid_username_error_message(self):
        error_message_element = self.get_element("xpath", self._invalid_username_error_message)
        actual_error_message = error_message_element.text
        expected_error_message = "Your username or password is invalid. Please try again."
        return self.ut.verify_text_contains(actual_error_message, expected_error_message)

    def verify_empty_username_error_message(self):
        error_message_element = self.get_element("xpath", self._empty_username_error_message)
        actual_error_message = error_message_element.text
        expected_error_message = "The email field is required."
        return self.ut.verify_text_contains(actual_error_message, expected_error_message)

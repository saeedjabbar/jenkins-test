import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions
from utilities.custom_logger import custom_logger
from utilities.util import Util


class CustomDriver():
    log = custom_logger()

    def __init__(self, driver):
        self.driver = driver
        self.ut = Util()

    def get_title(self):
        return self.driver.title

    def refresh(self):
        self.driver.refresh()

    def get_by_type(self, locator_type):
        """
        Return the By Type
        :param locator_type: CSS, XPath, Link, ID, Name
        :return:
        """
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        else:
            self.log.error("Locator Type:" + locator_type + "not correct/supported")
        return False

    def get_element(self, locator_type, locator):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info("Element found by locator type: " + locator_type + " and locator:" + locator)
        except:
            self.log.error("Element not found by locator type: " + locator_type + " and locator:" + locator)
        return element

    def get_elements(self, locator_type, locator):
        try:
            by_type = self.get_by_type(locator_type)
            element_list = self.driver.find_elements(by_type, locator)
            self.log.info("Element List found with locator type: " + locator_type + " and locator:" + locator)
        except:
            self.log.error("Element List not found with locator type: " + locator_type + " and locator:" + locator)
        return element_list

    def is_element_present(self, locator_type, locator):
        element_list = self.driver.find_elements(locator_type, locator)
        # element_list = self.get_elements(locator_type, locator)
        if len(element_list) > 0:
            self.log.info("Element with locator type: " + locator_type + " and locator:" + locator + " is present")
            return True
        else:
            self.log.error("Element with locator type: " + locator_type + " and locator:" + locator + " is not present")
            return False

    def wait_for_element(self, locator_type, locator, timeout=10, poll_frequency=.5):
        try:
            self.driver.implicitly_wait(0)
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum ::" + str(timeout) + ":: seconds for element to be visible")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                             ignored_exceptions=[NoSuchElementException, ElementNotInteractableException,
                                                 ElementNotVisibleException,
                                                 ElementClickInterceptedException])

            element = wait.until(expected_conditions.presence_of_element_located((by_type, locator)))
            self.log.info("Element with locator type: " + locator_type + " and locator:" + locator + " appeared on the web page")
        except:
            self.log.error("Element with locator type: " + locator_type + " and locator:" + locator + " not appeared on the web page")
        self.driver.implicitly_wait(3)
        return element

    def wait_for_element_clickable(self, locator_type, locator, timeout=10, poll_frequency=.5):
        try:
            self.driver.implicitly_wait(0)
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum ::" + str(timeout) + ":: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                             ignored_exceptions=[NoSuchElementException, ElementNotInteractableException,
                                                 ElementNotVisibleException,
                                                 ElementClickInterceptedException])

            element = wait.until(expected_conditions.element_to_be_clickable((by_type, locator)))
            self.log.info("Element with locator type: " + locator_type + " and locator:" + locator +  " appeared on the web page")
        except:
            self.log.error("Element with locator type: " + locator_type + " and locator:" + locator + " not appeared on the web page")
        self.driver.implicitly_wait(3)
        return element

    def click_element_when_ready(self, locator_type, locator, timeout=10, poll_frequency=.5):
        try:
            element = self.wait_for_element_clickable(locator_type, locator, timeout, poll_frequency)
            element.click()
            self.log.info("Element with locator type: " + locator_type + " and locator:" + locator + " clicked after wait")
        except:
            self.log.error("Element not clicked after wait")

    def send_keys_when_ready(self, data, locator_type, locator, clear=True, timeout=10, poll_frequency=.5):
        try:
            self.driver.implicitly_wait(0)
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum ::" + str(timeout) + ":: seconds for element to be visible")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException, ElementNotInteractableException,
                                                     ElementNotVisibleException,
                                                     ElementClickInterceptedException])

            element = wait.until(expected_conditions.visibility_of_element_located((by_type, locator)))
            self.log.info("Element with locator type: " + locator_type + " and locator: " + locator +
                     " appeared on the web page")
            if clear:
                element.clear()
            element.send_keys(data)
            self.log.info("Sending " + data + " to element with locator: " + locator)
        except:
            self.log.error("Element with locator type: " + locator_type + " and locator:" + locator +
                          " not appeared on the web page")
        self.driver.implicitly_wait(3)

    def get_text(self, locator_type, locator):
        """
        Gets text from the element with the provided locator and locator type
        :param locator_type: id/xpath/css/name
        :param locator: string value of the element locator
        :return:
        """
        try:
            element = self.get_element(locator_type, locator)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element with locator:" + locator)
                self.log.info("The text is: ", text)
        except:
            self.log.error("Failed to get text on element with locator " + locator)
        return text

    def select_current_month_checkin_date(self, date_to_select):
        locator = "//div[@id='calendar-searchboxdatepicker']//span[@data-date='{0}']".replace("{0}", date_to_select)
        element = self.get_element("xpath", locator)
        element.click()

    def select_current_month_checkin_date_for_loop(self, date_to_select):
        checkin_table = self.get_element("xpath", "(//nav[@data-testid='datepicker-tabs']//table[@class='aadb8ed6d3'])[1]")
        all_dates = checkin_table.find_elements(By.TAG_NAME, "span")
        for date in all_dates:
            if date.text == date_to_select:
                date.click()
                break

    def web_scroll(self, scroll_num="800", direction="up"):
        """
        Method to implement web scroll
        :param scroll_num: Number of pixels to scroll up or down
        :param direction: up/down
        :return: None
        """
        if direction == "down":
            self.driver.execute_script("window.scrollBy(0," + scroll_num + ")")
            self.log.info("Scrolled down with, " + scroll_num + " pixels")
        else:
            self.driver.execute_script("window.scrollBy(0,-" + scroll_num + ")")
            self.log.info("Scrolled up with, " + scroll_num + " pixels")

    def take_screenshot(self):
        filename = self.ut.get_random_timestamp_name() + ".png"
        folder_name = "../screenshots/"
        destination_file = self.ut.create_directory(folder_name) + filename
        self.driver.save_screenshot(destination_file)
        return destination_file

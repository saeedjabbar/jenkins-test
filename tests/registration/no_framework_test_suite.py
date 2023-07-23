import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def test_invalid_username():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.maximize_window()
    driver.get("https://www.letskodeit.com/")

    driver.find_element(By.XPATH, "//a[normalize-space()='Sign In']").click()
    driver.find_element(By.ID, "email").send_keys("")
    driver.find_element(By.ID, "login-password").send_keys("")
    time.sleep(1)
    driver.find_element(By.ID, "login").click()
    error_message_element = driver.find_element(By.XPATH, "//span[@class='dynamic-text help-block']")
    error_message_text = error_message_element.text
    print(error_message_text)
    driver.quit()


def test_empty_username():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.maximize_window()
    driver.get("https://www.letskodeit.com/")

    driver.find_element(By.XPATH, "//a[normalize-space()='Sign In']").click()
    driver.find_element(By.ID, "email").send_keys("")
    driver.find_element(By.ID, "login-password").send_keys("")
    time.sleep(1)
    driver.find_element(By.ID, "login").click()
    error_message_element = driver.find_element(By.XPATH, "//span[@class='error']")
    error_message_text = error_message_element.text
    print(error_message_text)
    driver.quit()
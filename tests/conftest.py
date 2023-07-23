import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function", autouse=True)
def setup_teardown_method():
    print("Method level setup")
    yield
    print("Method level teardown")

@pytest.fixture(scope="class", autouse=True)
def setup_teardown_class(request, browser):
    print("Class level setup")
    if browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)  # Set the page load timeout to 30 seconds
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Invalid browser option: {browser}")
        
    driver.implicitly_wait(3)
    driver.maximize_window()
    driver.get("https://www.letskodeit.com/")
    request.cls.driver = driver
    yield driver
    print("Class level teardown")
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to be used for testing (chrome/firefox)")
    parser.addoption("--os_type", action="store", default="mac",
                     help="Operating system type for testing (mac/windows/linux)")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def os_type(request):
    return request.config.getoption("--os_type")
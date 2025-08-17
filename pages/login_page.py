from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    BTN_LOGIN = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_LIST = (By.CSS_SELECTOR, "[data-test='inventory-list']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.base_url)

    def login(self, user: str, pwd: str):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME)).clear()
        self.driver.find_element(*self.USERNAME).send_keys(user)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(pwd)
        self.driver.find_element(*self.BTN_LOGIN).click()

    def assert_logged_in(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_LIST))

    def assert_error_contains(self, text: str):
        el = self.wait.until(EC.visibility_of_element_located(self.ERROR))
        assert text in el.text

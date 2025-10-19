from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    base_url = 'http://testshop.qa-practice.com'
    page_url = None

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open_page(self):
        if self.page_url:
            # гарантируем, что URL склеится правильно
            if not self.page_url.startswith("/"):
                self.page_url = "/" + self.page_url
            self.driver.get(f"{self.base_url}{self.page_url}")
        else:
            raise NotImplementedError("Page can not be opened for this page class")

    def find(self, locator: tuple, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator: tuple, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

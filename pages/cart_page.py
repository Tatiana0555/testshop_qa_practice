from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.locators import cart_locators as loc


class CartPage(BasePage):
    page_url = '/shop/cart'

    def check_page_section_title_is(self, text: str):
        order_overview = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.order_overview_loc)
        )
        actual_text = order_overview.get_attribute("textContent").strip()
        print(actual_text)
        assert actual_text == text, f"Ожидали '{text}', а получили '{actual_text}'"

    def check_message_in_the_section(self, text: str):
        empty_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.cart_empty_loc)
        )
        actual_text = empty_message.get_attribute("textContent").strip()
        print(actual_text)
        assert actual_text == text, f"Ожидали '{text}', а получили '{actual_text}'"

    def check_transition_to_logo(self):
        your_logo = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.click_your_loc)
        )
        your_logo.click()

        # 2. Ждём, пока произойдёт переход по адресу
        expected_url = "http://testshop.qa-practice.com/"
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))

        # 3. Проверяем текущий URL
        current_url = self.driver.current_url
        print(f"Текущий URL: {current_url}")

        assert current_url == expected_url, (
            f"Ожидали переход на {expected_url}, а оказались на {current_url}"
        )

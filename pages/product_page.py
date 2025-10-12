from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.locators import product_locators as loc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages.base_page import BasePage


class ProductPage(BasePage):
    page_url = '/shop/furn-9999-office-design-software-7?category=9'

    def check_page_terms_and_conditions(self, expected_text: str):

        terms_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc.terms_link_loc))
        terms_link.click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/terms"))

        standard_terms = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc.standard_terms_loc))
        actual_text = standard_terms.text.strip()
        print(f"Actual text: '{actual_text}'")

        assert actual_text == expected_text, f"Ожидали '{expected_text}', а получили '{actual_text}'"

        self.driver.back()

    def check_price_of_product_by_quantity(self, message: str):
        # 1. Считываем цену за одну единицу товара
        price_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.price_text_loc)
        )
        price_text = price_element.text.strip().replace(',', '')  # убираем запятые
        unit_price = float(price_text)
        print(f"Цена за одну единицу товара: {unit_price}")

        # 2. Увеличиваем количество товара на 4 клика
        plus_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(loc.plus_button_loc)
        )
        for _ in range(4):
            plus_button.click()

        # 3. Добавляем товар в корзину
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(loc.add_cart_button_loc)
        )
        add_button.click()

        # 4. Ждём появления уведомления
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc.alert))

        # 5. Переходим в корзину
        view_cart = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc.view_cart_loc))
        view_cart.click()

        # 6. уменьшаем кол-во товара на 1 единицу
        minus_in_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(loc.minus_in_cart_loc))

        # 7. Сохраняем старую сумму перед кликом
        old_cart_price = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.cart_price_text_loc)
        ).text.strip()

        minus_in_cart.click()

        # 8. Ждём, пока цена станет другой
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*loc.cart_price_text_loc).text.strip() != old_cart_price
        )

        # 9. Проверяем, что итоговая сумма = цена * количество
        quantity_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.quantity_input_loc)
        )
        quantity_value = int(quantity_input.get_attribute("value"))

        cart_price_el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.cart_price_text_loc)
        )
        cart_price_text = cart_price_el.text.strip().replace(',', '')
        cart_total = float(cart_price_text)

        expected_total = round(unit_price * quantity_value, 2)
        print(f"Ожидали: {expected_total}, получили: {cart_total}")

        assert cart_total == expected_total, (
            f"Ошибка: ожидали {expected_total}, а получили {cart_total}"
        )

        print(message)

    # попытка применить недействительный  промокод
    def check_invalid_promo_code(self, message: str):
        # 1. Добавляем товар в корзину
        add_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc.add_cart_button_loc))
        add_button.click()

        # 2. Ждём появления уведомления
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc.alert))

        # 3. Переходим в корзину
        view_cart = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc.view_cart_loc))
        view_cart.click()

        input_promo = self.driver.find_element(*loc.input_promo_loc)
        input_promo.send_keys('test')
        button_apply = self.driver.find_element(*loc.button_apply_loc)
        button_apply.click()

        # 4. Ожидание появления элемента
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc.alert_element_loc))
            print("Появилось предупреждение:", message)
        except TimeoutException:
            print("Предупреждение не появилось.")

    def check_required_fields_are_empty(self, message: str):
        #  Проверка выбора валюты и наличия уведомления о незаполненных полях при оформлении покупки
        # 1. Если выбор валюты доступен, то кликнуть по select_currency, если нет, то добавить товар в корзину
        try:
            select_currency = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc.select_currency_loc)
            )
            select_currency.click()

            # Выбираем "EUR"
            eur_option = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(loc.eur_option_loc)
            )
            eur_option.click()

            # Проверяем, что цена отображается в евро
            price_block = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(loc.price_block_loc)
            )
            price_text = price_block.text.strip()
            print("Текст цены:", price_text)
            assert "€" in price_text, f"Ожидали символ €, но получили: {price_text}"
            print("Цена отображается в евро:", price_text)
        except (NoSuchElementException, TimeoutException):

            # Если select_currency не найден, просто добавляем товар в корзину
            print("Кнопка выбора валюты не найдена, добавляем товар в корзину.")

        # 2. Добавляем товар в корзину
        add_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc.add_cart_button_loc))
        add_button.click()

        # 3. Ждём появления уведомления
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc.alert))

        # 4. Переходим в корзину
        view_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(loc.view_cart_loc)
        )
        view_cart.click()

        button_checkout = self.driver.find_element(*loc.button_checkout_loc)
        button_checkout.click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/address"))

        button_continue_checkout = self.driver.find_element(*loc.button_continue_checkout_loc)
        button_continue_checkout.click()

        # Проверяем, что на странице нужный текст уведомления
        note_empty_fields = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.note_empty_fields_loc)
        )
        assert note_empty_fields.text.strip() == "Some required fields are empty."

        print("Появилось предупреждение:", message)

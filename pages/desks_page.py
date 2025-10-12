from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.locators import category_locators as loc
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class DesksPage(BasePage):
    page_url = '/shop/category/desks-1'

    def check_name_desks_selected_category_is(self, text: str):
        selected_category = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(loc.desks_select_loc)
        )
        actual_text = selected_category.get_attribute("textContent").strip()
        print(f"Название категории: {actual_text}")
        assert actual_text == text, f"Ожидали '{text}', а получили '{actual_text}'"

    def check_sorted_price_low_to_high(self):
        # 1. Клик по кнопке дроп-меню
        dropdown_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(loc.dropdown_button_loc)
        )
        dropdown_button.click()

        # 2. Ожидание появления дроп-меню
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc.dropdown_menu_loc))

        # 3. Выбор сортировки "Price - Low to High"
        sorting_price_low_to_high = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(loc.price_low_to_high_loc))

        sorting_price_low_to_high.click()

        # 4. Ожидание, пока товары пересортируются и загрузятся
        product_elements = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(loc.product_elements_loc)
        )

        # 5. Собираем названия и цены
        products = []
        for product in product_elements:
            try:
                title = product.find_element(*loc.title_loc).text
                price_text = product.find_element(*loc.price_text_loc).text
                # Удаляем все нецифровые символы (кроме точки для дробных чисел)
                price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                products.append({"title": title, "price": price})
            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")

        # 6. Выводим список товаров по порядку от меньшей цены к большей
        print("Список товаров (от меньшей цены к большей):")
        for product in products:
            print(f"{product['title']} - {product['price']}")

        # 7. Проверяем, что товары отсортированы по возрастанию цены
        is_sorted = all(
            products[i]["price"] <= products[i + 1]["price"]
            for i in range(len(products) - 1)
        )

        # 8. Выводим результат проверки
        print(f"\nПроверка сортировки: {'Успешно' if is_sorted else 'Не успешно'}")
        assert is_sorted, "Товары не отсортированы по возрастанию цены!"

    def check_filter_by_components(self):
        # 1. Получаем исходный список товаров ДО фильтра
        initial_products = [
            el.text.strip()
            for el in WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(loc.product_locator_loc)
            )
        ]

        print(f"Исходный список товаров ({len(initial_products)} шт.):")
        for name in initial_products:
            print(f"   - {name}")

        # 2. Выбираем новый фильтр Components
        components = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(loc.components_loc))
        components.click()

        # 3. Ожидание изменения URL (если фильтр меняет адрес)
        WebDriverWait(self.driver, 20).until(EC.url_contains("components"))

        # 4. Ожидание появления элементов на обновлённой странице
        new_product_names = [
            el.text.strip()
            for el in WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(loc.new_list_produt_names))
        ]

        # 5. Вывод результата
        print('Список товаров после применения фильтра "Components":', new_product_names)

        # 6. Проверка, что фильтр сработал
        assert new_product_names != initial_products, (
            "Фильтр 'Components' не сработал: список товаров не изменился!"
        )
        assert len(new_product_names) < len(initial_products), (
            f"Фильтр 'Components' не уменьшил количество товаров: "
            f"было {len(initial_products)}, стало {len(new_product_names)}"
        )

        # 7. Вывод сообщения об успешном применении фильтра
        print(
            f"Фильтр 'Components' успешно применён! "
            f"Количество товаров: было {len(initial_products)}, стало {len(new_product_names)}."
        )

    def check_price_range(self):
        # 1. Разбираем текущий URL
        url = self.driver.current_url
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        # 2. Добавляем фильтр по цене
        params['min_price'] = ['300']
        params['max_price'] = ['2000']

        # 3. Формируем новый URL
        new_query = urlencode(params, doseq=True)
        new_url = urlunparse(parsed._replace(query=new_query))

        # 4. Переходим на новый URL
        self.driver.get(new_url)

        # 5. Проверка товаров
        products = self.driver.find_elements(*loc.products_loc)
        min_price = 300
        max_price = 2000
        invalid_products = []

        for product in products:
            try:
                name = product.find_element(*loc.name_loc).text
                price_text = product.find_element(*loc.price_text_loc).text
                # Убираем запятые из цены
                price_text = price_text.replace(",", "")
                price = float(price_text)
                print(f"{name}: {price} $")

                # Проверяем, что цена входит в диапазон
                if not (min_price <= price <= max_price):
                    invalid_products.append((name, price))

            except Exception as e:
                print("Ошибка в карточке:", e)

        # 6. Проверка результатов
        if invalid_products:
            for name, price in invalid_products:
                print(f"Товар '{name}' не соответствует диапазону цен: {price} $")
            assert False, f"Найдены товары вне диапазона цен {min_price}-{max_price} $"
        else:
            print(f"Все товары соответствуют диапазону цен {min_price}-{max_price} $")

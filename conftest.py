from selenium import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
from pages.desks_page import DesksPage
from pages.cart_page import CartPage
from pages.product_page import ProductPage


@pytest.fixture()
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")        # Отключает информационные панели
    options.add_argument("--disable-notifications")   # Отключает уведомления
    options.add_argument("--no-sandbox")              # Опция для контейнеров
    options.add_argument("--disable-dev-shm-usage")   # Для устранения проблем с памятью

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture()
def desks_page(driver):
    return DesksPage(driver)


@pytest.fixture()
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture()
def product_page(driver):
    return ProductPage(driver)

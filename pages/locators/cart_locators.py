from selenium.webdriver.common.by import By

order_overview_loc = (By.TAG_NAME, 'h3')
cart_empty_loc = (By.CLASS_NAME, 'js_cart_lines')
click_your_loc = (By.CSS_SELECTOR, 'a.navbar-brand.logo')
main_page_loc = (By.XPATH, '//*[@id="products_grid"]//li[1]//span')

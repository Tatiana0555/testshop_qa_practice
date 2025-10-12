def test_terms_and_conditions(product_page):
    product_page.open_page()
    product_page.check_page_terms_and_conditions('STANDARD TERMS AND CONDITIONS OF SALE')


def test_price_by_quantity(product_page):
    product_page.open_page()
    product_page.check_price_of_product_by_quantity('Цена соответствует цене по количеству товара')


def test_invalid_promo_code(product_page):
    product_page.open_page()
    product_page.check_invalid_promo_code('This promo code is not available')


def test_required_fields_empty(product_page):
    product_page.open_page()
    product_page.check_required_fields_are_empty('Some required fields are empty')

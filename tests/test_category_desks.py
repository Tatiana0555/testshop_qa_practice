def test_name_desks_selected_category(desks_page):
    desks_page.open_page()
    desks_page.check_name_desks_selected_category_is('Desks')


def test_check_sorted_price(desks_page):
    desks_page.open_page()
    desks_page.check_sorted_price_low_to_high()


def test_check_filter_by_components(desks_page):
    desks_page.open_page()
    desks_page.check_filter_by_components()


def test_check_price_range(desks_page):
    desks_page.open_page()
    desks_page.check_price_range()

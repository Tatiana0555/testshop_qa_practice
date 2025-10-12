def test_check_page_section_title_is(cart_page):
    cart_page.open_page()
    cart_page.check_page_section_title_is('Order overview')


def test_check_message_in_the_section(cart_page):
    cart_page.open_page()
    cart_page.check_message_in_the_section('Your cart is empty!')


def test_check_transition_to_logo(cart_page):
    cart_page.open_page()
    cart_page.check_transition_to_logo()

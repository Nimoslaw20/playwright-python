# sauce_page.py
from playwright.sync_api import Page

class SauceDemoPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.logo_text = page.get_by_text("Swag Labs")
        self.backpack_item = page.get_by_text("Sauce Labs Backpack")
        self.add_to_cart_button = page.get_by_role("button", name="Add to cart")
        self.cart_icon = page.locator('[data-test="shopping-cart-link"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator("#finish")
        self.thank_you_text = page.get_by_text('Thank you for your order!')
        self.back_to_products_button = page.locator("#back-to-products")

# test_sauce_demo.py
from playwright.sync_api import sync_playwright, expect
from pages.sauce_page import SauceDemoPage
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=2000)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    print(page.title())

    # Initialize Page Object
    sauce = SauceDemoPage(page)

    # Login
    sauce.username_input.type("standard_user")
    sauce.password_input.type("secret_sauce")
    sauce.login_button.click()
    expect(sauce.logo_text).to_be_visible(timeout=10000)
    print("Current URL:", page.url)
    expect(page).to_have_url(re.compile(r".*inventory\.html"))

    # Add to cart
    sauce.backpack_item.click()
    sauce.add_to_cart_button.click()
    sauce.cart_icon.click()

    # Checkout
    sauce.checkout_button.click()
    sauce.first_name_input.fill("John")
    sauce.last_name_input.fill("Doe")
    sauce.postal_code_input.fill("PO67")
    sauce.continue_button.click()
    sauce.finish_button.click()

    expect(sauce.thank_you_text).to_be_visible(timeout=10000)
    sauce.back_to_products_button.click()
    expect(sauce.logo_text).to_be_visible(timeout=10000)

    # browser.close()

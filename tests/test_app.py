# test_sauce_demo.py
from playwright.sync_api import sync_playwright, expect
from pages.sauce_page import SauceDemoPage
import re
import allure
import pytest

@allure.story("Sauce Demo E2E Test")
@allure.feature("Checkout Process")
def test_sauce_demo_checkout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=2000)
        context = browser.new_context()
        
        # Start tracing for better debugging
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        
        page = context.new_page()
        
        try:
            with allure.step("Navigate to Sauce Demo"):
                page.goto("https://www.saucedemo.com/")
                allure.attach(
                    page.screenshot(),
                    name="landing_page",
                    attachment_type=allure.attachment_type.PNG
                )
                print(page.title())

            # Initialize Page Object
            sauce = SauceDemoPage(page)

            with allure.step("Login"):
                sauce.username_input.type("standard_user")
                sauce.password_input.type("secret_sauce")
                sauce.login_button.click()
                expect(sauce.logo_text).to_be_visible(timeout=10000)
                print("Current URL:", page.url)
                expect(page).to_have_url(re.compile(r".*inventory\.html"))
                allure.attach(
                    page.screenshot(),
                    name="after_login",
                    attachment_type=allure.attachment_type.PNG
                )

            with allure.step("Add item to cart"):
                sauce.backpack_item.click()
                sauce.add_to_cart_button.click()
                sauce.cart_icon.click()
                allure.attach(
                    page.screenshot(),
                    name="cart_page",
                    attachment_type=allure.attachment_type.PNG
                )

            with allure.step("Complete checkout"):
                sauce.checkout_button.click()
                sauce.first_name_input.fill("John")
                sauce.last_name_input.fill("Doe")
                sauce.postal_code_input.fill("PO67")
                sauce.continue_button.click()
                sauce.finish_button.click()
                expect(sauce.thank_you_text).to_be_visible(timeout=10000)
                allure.attach(
                    page.screenshot(),
                    name="checkout_complete",
                    attachment_type=allure.attachment_type.PNG
                )

            with allure.step("Return to products"):
                sauce.back_to_products_button.click()
                expect(sauce.logo_text).to_be_visible(timeout=10000)

        except Exception as e:
            # Capture screenshot on failure
            allure.attach(
                page.screenshot(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
        finally:
            # Save trace data
            trace_path = "trace.zip"
            context.tracing.stop(path=trace_path)
            allure.attach.file(trace_path, name="playwright_trace", extension="zip")
            
            context.close()
            browser.close()
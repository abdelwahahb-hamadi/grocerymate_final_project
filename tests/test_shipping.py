from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import AuthPage
from pages.base_page import BasePage
from utils.constants import VALID_EMAIL, VALID_PASSWORD, CHECKOUT_URL


def _login(driver):
    auth = AuthPage(driver)
    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    auth.go_to_auth_after_login()
    assert auth.is_logged_in(), "Login failed: Logout not found on /auth."


def test_checkout_page_opens(driver):
    _login(driver)
    base = BasePage(driver)
    base.open(CHECKOUT_URL)

    # Page loaded: we should see at least one of these sections
    locator = (By.XPATH, "//*[contains(.,'Your products') or contains(.,'Shipment Address') or contains(.,'Payment')]")
    el = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
    assert el.is_displayed()


def test_shipping_rule_message_exists(driver):
    _login(driver)
    base = BasePage(driver)
    base.open(CHECKOUT_URL)

    # The rule text: "Free shipment if your purchase is 20€ or more."
    locator = (By.XPATH, "//*[contains(.,'Free shipment') and contains(.,'20')]")
    el = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
    assert el.is_displayed()


def test_checkout_totals_labels_exist(driver):
    _login(driver)
    base = BasePage(driver)
    base.open(CHECKOUT_URL)

    # Labels exist (works even if cart is empty)
    product_total = (By.XPATH, "//*[normalize-space()='Product Total:']")
    shipment = (By.XPATH, "//*[normalize-space()='Shipment:']")
    total = (By.XPATH, "//*[normalize-space()='Total:']")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(product_total))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(shipment))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(total))

    assert driver.find_element(*product_total).is_displayed()
    assert driver.find_element(*shipment).is_displayed()
    assert driver.find_element(*total).is_displayed()
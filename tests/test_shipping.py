from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import AuthPage
from pages.store_page import StorePage
from pages.base_page import BasePage
from utils.constants import VALID_EMAIL, VALID_PASSWORD, CHECKOUT_URL
from utils.helpers import dob_for_age_years


def _login_and_pass_age(driver):
    auth = AuthPage(driver)
    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    auth.go_to_auth_after_login()
    assert auth.is_logged_in(), "Login failed: Logout not found on /auth."

    store = StorePage(driver)
    store.open_store()
    store.complete_age_verification(dob_for_age_years(18))
    store.assert_age_verified_success()


def test_shipping_rule_message_exists(driver):
    _login_and_pass_age(driver)

    base = BasePage(driver)
    base.open(CHECKOUT_URL)

    locator = (By.XPATH, "//*[contains(.,'Free shipment') and contains(.,'20')]")
    el = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
    assert el.is_displayed(), "Shipping rule message not visible on checkout page."
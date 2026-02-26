import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import AuthPage
from pages.store_page import StorePage
from utils.constants import VALID_EMAIL, VALID_PASSWORD
from utils.helpers import dob_for_age_years


def _login(driver):
    auth = AuthPage(driver)
    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)
    auth.go_to_auth_after_login()
    assert auth.is_logged_in(), "Login failed: Logout not found on /auth."
    return auth


def test_age_modal_appears_on_store(driver):
    _login(driver)
    store = StorePage(driver)
    store.open_store()
    assert store.is_visible(store.AGE_MODAL), "Expected Age Verification modal to appear on store page."


@pytest.mark.parametrize("age_years", [18, 25])
def test_age_verification_allows_access(driver, age_years):
    _login(driver)
    store = StorePage(driver)
    store.open_store()
    store.complete_age_verification(dob_for_age_years(age_years))
    store.assert_age_verified_success()


def test_age_verification_modal_disappears_after_success(driver):
    _login(driver)
    store = StorePage(driver)
    store.open_store()
    store.complete_age_verification(dob_for_age_years(25))
    store.wait_invisible(store.AGE_MODAL)
    assert not store.is_visible(store.AGE_MODAL), "Age modal should be gone after successful verification."


@pytest.mark.parametrize("age_years", [17])
def test_age_verification_underage_shows_message(driver, age_years):
    _login(driver)
    store = StorePage(driver)
    store.open_store()
    store.complete_age_verification(dob_for_age_years(age_years))

    locator = (By.XPATH, "//*[contains(.,'You are underage') or contains(.,'underage')]")
    el = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
    assert el.is_displayed(), "Expected underage message, but it did not appear."

def test_age_verification_empty_input_shows_toast(driver):
    _login(driver)
    store = StorePage(driver)
    store.open_store()

    assert store.is_visible(store.AGE_MODAL), "Age modal did not appear on store page."
    store.type(store.AGE_INPUT, "", clear=True)
    store.click(store.AGE_CONFIRM)

    # Expect any toast/alert after invalid submit
    locator = (By.XPATH, "//*[contains(@class,'toast') or contains(@class,'Toast') or contains(@class,'alert') or contains(.,'underage') or contains(.,'Invalid') or contains(.,'required')]")
    el = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
    assert el.is_displayed(), "Expected an error/toast message for empty DOB, but none appeared."


def test_age_verification_invalid_format_shows_toast(driver):
    _login(driver)
    store = StorePage(driver)
    store.open_store()

    assert store.is_visible(store.AGE_MODAL), "Age modal did not appear on store page."
    store.type(store.AGE_INPUT, "abc", clear=True)
    store.click(store.AGE_CONFIRM)

    locator = (By.XPATH, "//*[contains(@class,'toast') or contains(@class,'Toast') or contains(@class,'alert') or contains(.,'underage') or contains(.,'Invalid') or contains(.,'required')]")
    el = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
    assert el.is_displayed(), "Expected an error/toast message for invalid DOB format, but none appeared."
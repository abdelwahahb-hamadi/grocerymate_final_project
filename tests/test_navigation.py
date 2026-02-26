from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import AuthPage
from pages.base_page import BasePage
from pages.store_page import StorePage
from utils.constants import VALID_EMAIL, VALID_PASSWORD, BASE_URL
from utils.helpers import dob_for_age_years


def _login(driver):
    auth = AuthPage(driver)
    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    auth.go_to_auth_after_login()
    assert auth.is_logged_in(), "Login failed: Logout not found on /auth."


def _pass_age(driver):
    store = StorePage(driver)
    store.open_store()
    store.complete_age_verification(dob_for_age_years(18))
    # success toast appears in your StorePage
    store.assert_age_verified_success()


def test_store_page_has_search(driver):
    _login(driver)
    _pass_age(driver)

    # In store header there is search input "Search Products"
    locator = (By.XPATH, "//input[contains(@placeholder,'Search') or contains(@aria-label,'Search')]")
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    assert el is not None


def test_favorites_page_opens(driver):
    _login(driver)
    _pass_age(driver)

    base = BasePage(driver)
    base.open(BASE_URL + "/favorites")

    # Page loaded: Favorites title or empty state
    locator = (By.XPATH, "//*[contains(.,'Favorites') or contains(.,'favourites') or contains(.,'No favorites')]")
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    assert el is not None
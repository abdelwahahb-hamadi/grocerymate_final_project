import pytest
from pages.auth_page import AuthPage
from pages.store_page import StorePage
from utils.constants import VALID_EMAIL, VALID_PASSWORD
from utils.helpers import dob_for_age_years


@pytest.mark.parametrize("age_years", [18])
def test_age_verification_allows_access(driver, age_years):
    auth = AuthPage(driver)
    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    auth.go_to_auth_after_login()
    assert auth.is_logged_in(), "Login failed: Logout button not found on /auth."

    store = StorePage(driver)
    store.open_store()
    store.complete_age_verification(dob_for_age_years(age_years))
    store.assert_age_verified_success()
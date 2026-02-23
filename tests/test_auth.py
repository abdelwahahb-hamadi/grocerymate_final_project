from pages.auth_page import AuthPage
from utils.constants import VALID_EMAIL, VALID_PASSWORD


def test_login_success(driver):
    auth = AuthPage(driver)

    # 1) Login on /auth
    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    # 2) Confirm we are redirected to home
    auth.assert_redirected_to_home()

    # 3) Open /auth again (Logout is shown there when logged in)
    auth.go_to_auth_after_login()

    # 4) Assertion
    assert auth.is_logged_in(), "Expected Logout button on /auth after login, but it didn't appear."
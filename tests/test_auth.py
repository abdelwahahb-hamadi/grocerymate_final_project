import pytest
from pages.auth_page import AuthPage
from utils.constants import VALID_EMAIL, VALID_PASSWORD


def test_login_success(driver):
    auth = AuthPage(driver)

    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    auth.assert_redirected_to_home()

    auth.go_to_auth_after_login()
    assert auth.is_logged_in(), "Expected Logout button on /auth after login, but it didn't appear."


def test_logout_success(driver):
    auth = AuthPage(driver)

    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    auth.go_to_auth_after_login()
    assert auth.is_logged_in(), "Expected Logout button on /auth after login, but it didn't appear."

    auth.logout()
    assert auth.is_visible(auth.SIGN_IN), "Expected Sign In button after logout, but it didn't appear."


@pytest.mark.parametrize(
    "email,password",
    [
        (VALID_EMAIL, "wrong-password-123"),
        ("wrong_email@example.com", VALID_PASSWORD),
    ],
)
def test_login_invalid_credentials(driver, email, password):
    auth = AuthPage(driver)

    auth.open_auth()
    auth.login_attempt(email, password)

    assert "/auth" in auth.driver.current_url, f"Expected to stay on /auth on failed login, got: {auth.driver.current_url}"
    assert not auth.is_logged_in(), "Unexpectedly found Logout button. Login should have failed."
    assert auth.is_visible(auth.SIGN_IN), "Expected Sign In button to remain visible after failed login."
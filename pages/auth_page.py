from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.constants import AUTH_URL, BASE_URL


class AuthPage(BasePage):
    EMAIL = (By.XPATH, "//input[@name='email' or @type='email']")
    PASSWORD = (By.XPATH, "//input[@name='password' or @type='password']")
    SIGN_IN = (By.XPATH, "//button[@type='submit' or normalize-space()='Sign In' or normalize-space()='Sign in']")
    LOGOUT = (By.XPATH, "//button[normalize-space()='Logout']")

    def open_auth(self):
        self.open(AUTH_URL)

    def login_attempt(self, email: str, password: str):
        """Click Sign In without assuming success (used for negative tests)."""
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.SIGN_IN)

    def login(self, email: str, password: str):
        """Login expecting success -> wait for redirect away from /auth."""
        self.login_attempt(email, password)
        self.wait.until(lambda d: "/auth" not in d.current_url)

    def go_to_auth_after_login(self):
        self.open_auth()

    def is_logged_in(self) -> bool:
        return self.is_visible(self.LOGOUT)

    def logout(self):
        self.click(self.LOGOUT)

    def assert_redirected_to_home(self):
        url = self.driver.current_url.rstrip("/")
        assert url == BASE_URL, f"Expected redirect to home, but got: {self.driver.current_url}"
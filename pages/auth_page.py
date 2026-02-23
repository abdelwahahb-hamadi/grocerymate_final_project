from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.constants import AUTH_URL, BASE_URL


class AuthPage(BasePage):
    EMAIL = (By.XPATH, "//input[@name='email' or @type='email']")
    PASSWORD = (By.XPATH, "//input[@name='password' or @type='password']")
    SIGN_IN = (By.XPATH, "//button[@type='submit' or normalize-space()='Sign In' or normalize-space()='Sign in']")
    LOGOUT = (By.XPATH, "//button[normalize-space()='Logout']")

    def open_auth(self):
        self.open(AUTH_URL)

    def login(self, email: str, password: str):
        """
        Real behavior:
        - You sign in on /auth
        - App redirects you to Home (/)
        - Logout button appears only when you open /auth again
        """
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.SIGN_IN)

        # Wait until we leave /auth (redirect to home or any other page)
        self.wait.until(lambda d: "/auth" not in d.current_url)

    def go_to_auth_after_login(self):
        """Open /auth again to see Logout button (as you do manually)."""
        self.open_auth()

    def is_logged_in(self) -> bool:
        """On /auth when logged in, Logout button is visible."""
        return self.is_visible(self.LOGOUT)

    def assert_redirected_to_home(self):
        # home can be BASE_URL or BASE_URL + '/'
        url = self.driver.current_url.rstrip("/")
        assert url == BASE_URL, f"Expected redirect to home, but got: {self.driver.current_url}"
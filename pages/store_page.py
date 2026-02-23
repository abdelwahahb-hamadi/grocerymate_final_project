from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.constants import STORE_URL

class StorePage(BasePage):
    AGE_MODAL = (By.XPATH, "//div[contains(.,'Age Verification') and .//*[contains(.,'Please enter your birth date')]]")
    AGE_INPUT = (By.XPATH, "//input[@placeholder='DD-MM-YYYY' or contains(@placeholder,'DD') and contains(@placeholder,'YYYY')]")
    AGE_CONFIRM = (By.XPATH, "//button[normalize-space()='Confirm']")
    AGE_TOAST_SUCCESS = (By.XPATH, "//*[contains(.,'You are of age') and contains(.,'even alcohol products')]")

    def open_store(self):
        self.open(STORE_URL)

    def complete_age_verification(self, dob_dd_mm_yyyy: str):
        # Wait modal
        assert self.is_visible(self.AGE_MODAL), "Age modal did not appear on store page."
        self.type(self.AGE_INPUT, dob_dd_mm_yyyy)
        self.click(self.AGE_CONFIRM)

    def assert_age_verified_success(self):
        # Either toast appears OR modal disappears (we do both)
        assert self.is_visible(self.AGE_TOAST_SUCCESS), "Success toast did not appear."
        self.wait_invisible(self.AGE_MODAL)
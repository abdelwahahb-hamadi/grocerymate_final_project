from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import AuthPage
from pages.base_page import BasePage
from utils.constants import VALID_EMAIL, VALID_PASSWORD

PRODUCT_URL = "https://grocerymate.masterschool.com/product/66b3a57b3fd5048eacb47998"


def test_rating_section_visible(driver):
    auth = AuthPage(driver)
    auth.open_auth()
    auth.login(VALID_EMAIL, VALID_PASSWORD)

    base = BasePage(driver)
    base.open(PRODUCT_URL)

    # Assert product title exists (page loaded)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Gala Apples']"))
    )

    # Assert rating stars area exists (rating feature present)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'star') or .//*[name()='svg' and contains(@class,'star')] or contains(.,'(')]"))
    )
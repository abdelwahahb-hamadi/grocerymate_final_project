from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.constants import DEFAULT_TIMEOUT, POLL_FREQUENCY

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT, poll_frequency=POLL_FREQUENCY)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, by):
        return self.driver.find_element(*by)

    def finds(self, by):
        return self.driver.find_elements(*by)

    def click(self, by):
        self.wait.until(EC.element_to_be_clickable(by)).click()

    def type(self, by, text: str, clear: bool = True):
        el = self.wait.until(EC.visibility_of_element_located(by))
        if clear:
            el.clear()
        el.send_keys(text)
        return el

    def is_visible(self, by) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(by))
            return True
        except TimeoutException:
            return False

    def wait_invisible(self, by) -> bool:
        return self.wait.until(EC.invisibility_of_element_located(by))

    def text_of(self, by) -> str:
        el = self.wait.until(EC.visibility_of_element_located(by))
        return el.text.strip()

    def wait_text_contains(self, by, fragment: str):
        return self.wait.until(EC.text_to_be_present_in_element(by, fragment))
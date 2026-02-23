import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.constants import SCREENSHOTS_DIR, REPORTS_DIR
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

@pytest.fixture(scope="session", autouse=True)
def _ensure_dirs():
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

@pytest.fixture()
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1400,900")
    # options.add_argument("--headless=new")  # enable later if you want
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    drv.implicitly_wait(0)  # we rely on explicit waits

    yield drv

    drv.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver", None)
        if drv:
            path = SCREENSHOTS_DIR / f"{item.name}.png"
            drv.save_screenshot(str(path))
            # Attach path to report
            rep.extra = getattr(rep, "extra", [])
            rep.extra.append({"name": "screenshot", "path": str(path)})
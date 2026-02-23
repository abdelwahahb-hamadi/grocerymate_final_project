import os
from pathlib import Path

BASE_URL = "https://grocerymate.masterschool.com"
AUTH_URL = f"{BASE_URL}/auth"
STORE_URL = f"{BASE_URL}/store"
CHECKOUT_URL = f"{BASE_URL}/checkout"

# Product we used
GALA_APPLES_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47998"
GALA_APPLES_NAME = "Gala Apples"

# Credentials (prefer env vars)
VALID_EMAIL = os.getenv("MM_EMAIL", "abdelwahab.hamadi@outlook.com")
VALID_PASSWORD = os.getenv("MM_PASSWORD", "123456789")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Timeouts
DEFAULT_TIMEOUT = 12
POLL_FREQUENCY = 0.2
from pathlib import Path

BASE_URL = "https://www.jumia.co.ke"
HOME_PAGE = f"{BASE_URL}/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
REQUEST_DELAY = 2

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA = PROJECT_ROOT / "data" / "raw"

RAW_HOME = RAW_DATA / "homepage"
RAW_CATEGORIES = RAW_DATA / "categories"
RAW_PRODUCTS = RAW_DATA / "products"

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
LOGS = PROJECT_ROOT / "data" / "logs"
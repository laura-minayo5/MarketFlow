# fetches the HTML content of a given URL using the requests library. 
# It sets up a session with custom headers and a timeout, then performs a GET request to retrieve the page content. 
# If the request is successful, it returns the HTML text; otherwise, it raises an HTTP error.
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.paths import HEADERS, MAX_RETRIES, REQUEST_TIMEOUT

# Set up a retry strategy for handling transient errors and rate limiting.
# The retry strategy specifies the total number of retries, a backoff factor for exponential backoff,
# a list of HTTP status codes that should trigger a retry, and the allowed HTTP methods for retries.
retry_strategy = Retry(
    total=MAX_RETRIES,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)

# Create a session object to persist settings across requests, including headers and retry strategy.
session = requests.Session()
session.headers.update(HEADERS)

# Mount the retry strategy to the session for both HTTP and HTTPS requests.
adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)


def download_page(url: str) -> str:
    """Download a web page and return its HTML."""

    response = session.get(
    url,
    timeout=REQUEST_TIMEOUT,
    )

    print(response.url)
    print(response.status_code)

    response.raise_for_status()

    return response.text
    
    # response = session.get(
    #     url,
    #     timeout=REQUEST_TIMEOUT,
    # )

    # response.raise_for_status()

    # return response.text
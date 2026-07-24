# Parser -> transforms HTML into structured data.

# Input: Jumia homepage HTML.
# Work: Extract category names and relative URLs from the Jumia homepage using BeautifulSoup.
# Output: a dictionary consisting of category names and their corresponding URLs.

# Homepage html
#     ↓ 
# Extract Category Names and URLs
#     ↓
# Return a dictionary of category names and URLs

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.paths import BASE_URL


def extract_category_urls(html: str) -> dict[str, str]:
    """Extract category names and relative URLs from the Jumia homepage."""

    soup = BeautifulSoup(html, "lxml")

    categories = {}

    # Select every category link (<a>) that has
    # class="itm" and an href attribute.
    links = soup.select("a.itm[href]")
    for link in links:

        # Retrieve the href attribute.
        # Use get() for HTML attributes (metadata).
        href = link.get("href")

        # Find the child <span> containing the category name.
        # Use find() (or select_one()) for child elements.
        # span = link.find("span", class_="text")
        span = link.select_one("span.text")

        # Skip malformed links that are missing
        # either the URL or the category name.
        if not href or not span:
            continue

        name = span.get_text(strip=True)

        categories[name] = urljoin(BASE_URL, href)


    return categories
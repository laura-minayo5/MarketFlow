# Parser -> transforms HTML into structured data.
# Parses the product URLs from a category page.

# Input: HTML of a category page.
# Work: Extract product names and relative URLs from a Jumia category page using BeautifulSoup.
# Output: a dictionary consisting of product names and their corresponding URLs.

# Category HTML from category_crawler.py
#       ↓
# Extract Product Names and URLs
#       ↓
# Return a dictionary of product names and URLs

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from config.paths import BASE_URL


def extract_product_urls(html: str) -> dict[str, str]:
    """Extract product names and URLs from a category page."""

    soup = BeautifulSoup(html, "lxml")

    products = {}

    # Select every product card (<article>) with class="prd".
    product_cards = soup.select("article.prd")

    for card in product_cards:

        # Find the product link.
        link = card.select_one("a.core")

        if not link:
            continue

        # Retrieve the href attribute.
        href = link.get("href")

        if not href:
            continue

        # Find the product name.
        title = card.select_one("div.name")

        if not title:
            continue

        name = title.get_text(strip=True)

        # Convert relative URLs to absolute URLs.
        products[name] = urljoin(BASE_URL, href)

    return products
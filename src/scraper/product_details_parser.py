# Parser -> transforms HTML into structured data.
# Parses the product details from a product page.
# Input: HTML of a product page.
# Work: Extract product details such as name, price, old price, discount, rating, and reviews from a Jumia product page using BeautifulSoup.
# Output: a dictionary of product details.

# Product HTML
#      ↓
# Extract Product Details
#      ↓
# Return a dictionary of product details

from bs4 import BeautifulSoup


def parse_product_details(html: str) -> dict[str, str | None]:
    """Extract product details from a product page."""

    soup = BeautifulSoup(html, "lxml")

    def text(selector: str) -> str | None:
        """Return the text for a CSS selector or None."""

        element = soup.select_one(selector)

        if element:
            return element.get_text(strip=True)

        return None

    return {
        "name": text("h1"),
        "price": text(".-b.-ltr.-tal.-fs24.-prxs"),
        "old_price": text(".-tal.-gy5.-lthr.-fs16"),
        "discount": text(".bdg._dsct"),
        "rating": text(".-fs29.-yl5.-pvxs"),
        "reviews": text(".-plxs._more"),
    }
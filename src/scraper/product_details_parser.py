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


def get_text(soup: BeautifulSoup, selector: str) -> str | None:
    """
    Return the text of the first element matching the CSS selector.
    Returns None if the element does not exist.
    """

    element = soup.select_one(selector)

    if element:
        return element.get_text(strip=True)

    return None


def get_brand(soup: BeautifulSoup) -> str | None:
    """
    Extract the product brand.
    The brand section looks like:
    <div class="-pvxs">
        Brand:
        <a ...>EAGEAT</a>
    </div>
    Return only the brand name.
    """

    brand_section = soup.select_one("div.-pvxs")

    if not brand_section:
        return None

    brand_link = brand_section.find("a")

    if not brand_link:
        return None

    return brand_link.get_text(strip=True)


def parse_product_details(html: str) -> dict[str, str | None]:
    """
    Extract structured product information from a Jumia product page.
    """

    soup = BeautifulSoup(html, "lxml")

    product = {
        "name": get_text(soup, "h1"),
        "brand": get_brand(soup),
        "current_price": get_text(soup, "span.-b.-fs24"),
        "old_price": get_text(soup, "span.-lthr"),
        "discount": get_text(soup, "span[data-disc]"),
        "availability": get_text(soup, "p.-df.-i-ctr.-fs12"),
        "rating": get_text(soup, "div.stars"),
        "reviews": get_text(soup, "a.-plxs._more"),
    }

    return product
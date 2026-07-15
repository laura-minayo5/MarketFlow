# Parser -> transforms HTML into structured data.
# Parses the product details from a product page.
# Input: HTML of a product page.
# Work: Extract product details such as name, price, old price, discount, rating, and reviews from a Jumia product page using BeautifulSoup.
# Output: a dictionary of product details.

# Product HTML from product_crawler.py
#      ↓
# Extract Product Details
#      ↓
# Return a dictionary of product details

from bs4 import BeautifulSoup
import re
from typing import Any

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

def get_description(soup: BeautifulSoup) -> str | None:
    """
    Extract the product description.
    Returns all visible text from the Product Details section.
    """

    description_section = soup.select_one("div.markup")

    if not description_section:
        return None

    # using stripped_strings collects all the visible text while automatically ignoring empty tags and images.
    parts = list(description_section.stripped_strings)

    return " ".join(parts) if parts else None


def parse_markup(markup: BeautifulSoup) -> dict | list | str | None:
    """
    Parse the contents of a specification section.

    Returns:
        - dict: if the section contains key-value pairs.
        - list: if the section contains a simple list.
        - str: if the section contains plain text.
        - None: if no content exists.
    """

    items = markup.select("li")

    # No list items -> just return the text.
    if not items:
        text = " ".join(markup.stripped_strings)
        return text if text else None

    data_dict = {}
    data_list = []

    for item in items:

        strong = item.find("strong")

        # Case 1: key-value pair.
        if strong:

            key = strong.get_text(strip=True).rstrip(":")

            text = item.get_text(" ", strip=True)

            value = text.replace(strong.get_text(strip=True), "").strip()

            data_dict[key] = value

        # Case 2: plain list item.
        else:

            data_list.append(item.get_text(" ", strip=True))

    if data_dict:
        return data_dict

    return data_list


def get_product_sections(soup: BeautifulSoup) -> dict[str, dict | list | str]:
    """
    Extract all structured product sections.

    Examples:
        - Key Features
        - Specifications
        - What's in the box
        - Warranty
    """

    sections = {}

    for article in soup.select("section article.col8"):

        heading = article.select_one("h3")

        markup = article.select_one("div.markup")

        if not heading or not markup:
            continue

        title = heading.get_text(strip=True)

        sections[title] = parse_markup(markup)

    return sections

def get_breadcrumbs(soup: BeautifulSoup) -> list[str]:
    """
    Extract the breadcrumb trail.

    Example:
    Home > Computing > Laptops > Business Laptops > HP EliteBook
    """

    container = soup.select_one("div.brcbs")

    if not container:
        return []

    breadcrumbs = []

    # Both <a> and <span> are breadcrumb items, 
    # so select both (a.cbs, span.cbs) or use a common class (cbs)
    for crumb in container.select(".cbs"):

        text = crumb.get_text(strip=True)

        if text:
            breadcrumbs.append(text)

    return breadcrumbs

def get_seller(soup: BeautifulSoup) -> str | None:
    """
    Extract the seller name.
    """

    seller = soup.select_one("div.-hr.-pam > p.-m.-pbm")

    if seller:
        return seller.get_text(strip=True)

    return None

def get_seller_performance(soup: BeautifulSoup) -> dict[str, str]:
    """
    Extract seller performance metrics.
    """

    performance = {}

    section = soup.find("h3", string="Seller Performance")

    if not section:
        return performance

    container = section.find_parent("div")

    if not container:
        return performance

    for row in container.select("div.-df.-i-ctr.-ptm"):

        p = row.find("p")

        if not p:
            continue

        span = p.find("span")

        if not span:
            continue

        metric = p.get_text(" ", strip=True).replace(span.get_text(strip=True), "").replace(":", "").strip()

        performance[metric] = span.get_text(strip=True)

    return performance

def get_reviews(soup: BeautifulSoup) -> str | None:
    """
    Extract the number of verified ratings.
    Returns only the numeric value.
    """

    reviews = get_text(soup, "a.-plxs._more")

    if not reviews:
        return None

    match = re.search(r"\d+", reviews)

    if match:
        return match.group()

    return None

def get_rating(soup: BeautifulSoup) -> str | None:
    rating = get_text(soup, "div.stars")

    if not rating:
        return None

    return rating.split()[0]


def parse_product_details(html: str,) -> dict[str, Any]:
    """
    Extract structured product information from a Jumia product page.
    """

    soup = BeautifulSoup(html, "lxml")

    product = {
    "name": get_text(soup, "h1"),
    "brand": get_brand(soup),
    "breadcrumbs": get_breadcrumbs(soup),

    "current_price": get_text(soup, "span.-b.-fs24"),
    "old_price": get_text(soup, "span.-lthr"),
    "discount": get_text(soup, "span[data-disc]"),
    "availability": get_text(soup, "p.-df.-i-ctr.-fs12"),

    "rating": get_rating(soup),
    "reviews": get_reviews(soup),

    "description": get_description(soup),

    "seller": get_seller(soup),
    "seller_performance": get_seller_performance(soup),

    "product_sections": get_product_sections(soup),
    }

    return product
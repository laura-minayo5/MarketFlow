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


def clean_text(text: str) -> str:
    """
    Normalize text extracted from HTML.

    - Replace HTML non-breaking spaces (&nbsp;) with normal spaces.
    - Collapse multiple whitespace characters into a single space.
    - Remove leading and trailing whitespace.
    """

    return re.sub(
        r"\s+",
        " ",
        text.replace("\xa0", " ")
    ).strip()

def get_text(soup: BeautifulSoup, selector: str) -> str | None:
    """
    Return the cleaned text of the first element matching the CSS selector.
    Returns None if the element does not exist.
    """

    element = soup.select_one(selector)

    if not element:
        return None

    return clean_text(element.get_text(" ", strip=True))


def get_brand(soup: BeautifulSoup) -> str | None:
    """
    Extract the product brand.

    HTML structure:

    <div class="-phm">
        <div class="-pvxs">
            Brand:
            <a class="_more">Vision Plus</a>
        </div>
    </div>
    CSS selector:
        div.-phm div.-pvxs a._more

    This means:
        div.-phm      -> product information section
            div.-pvxs -> brand information block
                a._more -> brand name link
    """

    # Select the brand link from the product information section.
    brand = soup.select_one("div.-phm div.-pvxs a._more")

    if not brand:
        return None

    return clean_text(brand.get_text(" ", strip=True))

def get_description(soup: BeautifulSoup) -> str | None:
    """
    Extract the Product Details description.

    The Product Details section has the structure:

    <div class="card">
        <div id="description"></div>
        <header>
            <h2>Product details</h2>
        </header>
        <div class="markup">...</div>
    </div>

    We first locate the unique description anchor, then find the
    surrounding card, and finally extract the text from the markup
    inside that card.
    """

    # Find the unique Product Details anchor.
    description_anchor = soup.select_one("div#description")

    if not description_anchor:
        return None

    # Move to the surrounding card.
    card = description_anchor.find_parent("div", class_="card")

    if not card:
        return None

    # Find the markup that belongs only to Product Details.
    markup = card.select_one("div.markup")

    if not markup:
        return None
    
    descriptive_parts = []
    
    for element in markup.find_all(["p", "li"]):
        text = clean_text(element.get_text(" ", strip=True))
        if text:
            descriptive_parts.append(text)

    # Return the joined parts or None if no parts exist.
    return "\n\n".join(descriptive_parts) if descriptive_parts else None


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
        text = clean_text(" ".join(markup.stripped_strings))
        return text if text else None

    specifications = {}
    features = []

    for item in items:

        strong = item.find("strong")

        # Case 1: key-value pair.
        if strong:
            key = clean_text(strong.get_text()).rstrip(":")

            text = clean_text(item.get_text(" ", strip=True))

            value = text.replace(key, "").strip()

            specifications[key] = value

        # Case 2: plain list item.
        else:

            features.append(clean_text(item.get_text(" ", strip=True)))

    if specifications:
        return specifications

    return features


def get_product_sections(soup: BeautifulSoup) -> dict[str, dict | list | str | None]:
    """
    Extract all structured product information sections.

    Each section consists of a heading and its corresponding content,
    which is parsed by `parse_markup()`.

    Examples:
        - Key Features
        - Specifications
        - What's in the box
        - Warranty

    Returns:
        A dictionary mapping each section title to its parsed content.
    """
    sections = {}

    for article in soup.select("section article.col8"):

        heading = article.select_one("h3")

        markup = article.select_one("div.markup")

        if not heading or not markup:
            continue

        title = clean_text(heading.get_text(strip=True))

        sections[title] = parse_markup(markup)

    return sections

def get_breadcrumbs(soup: BeautifulSoup) -> list[str]:
    """
    Extract the breadcrumb navigation trail.

    Example:
        Home > Computing > Laptops > Business Laptops

    Returns:
        A list of category breadcrumb labels in order from the
        homepage to the product's category.
    """

    container = soup.select_one("div.brcbs")

    if not container:
        return []

    breadcrumbs = []

    # Category breadcrumbs are stored in <a class="cbs"> elements.
    # The product name is stored separately in a <span class="cbs">,
    # so selecting only anchor tags excludes the product name.
    for crumb in container.select("a.cbs"):

        text = clean_text(crumb.get_text(" ", strip=True))

        if text:
            breadcrumbs.append(text)

    return breadcrumbs

def get_seller(soup: BeautifulSoup) -> str | None:
    """
    Extract the seller name from the seller information section.

    Returns:
        The seller name, or None if the product has no seller information.
    """

    seller = soup.select_one("div.-hr.-pam > p.-m.-pbm")

    if not seller:
        return None

    return clean_text(seller.get_text(" ", strip=True))

def get_seller_performance(soup: BeautifulSoup) -> dict[str, str]:
    """
    Extract the seller performance metrics.
    HTML structure:
    <div class="-df -i-ctr -ptm">
        <p>
            Shipping speed:
            <span class="-m">Excellent</span>
        </p>
    </div>

    Returns a dictionary such as:
    {
        "Shipping speed": "Excellent",
        "Quality Score": "Excellent",
        "Customer Rating": "Good",
        "Cancellation Rate": "Excellent"
    }
    """
    performance = {}

    # Each seller performance metric is stored in its own row.
    for row in soup.select("div.-df.-i-ctr.-ptm"):

        p = row.find("p")
        if not p:
            continue

        value = p.find("span")
        if not value:
            continue

        value_text = clean_text(value.get_text())

        metric = clean_text(
            p.get_text(" ", strip=True)
            .replace(value.get_text(strip=True), "")
            .replace(":", "")
            .strip()
        )

        performance[metric] = value_text

    return performance

def get_reviews(soup: BeautifulSoup) -> str | None:
    """
    Extract the number of product ratings.

    Returns:
        The numeric rating count as a string, or None if unavailable.
    """

    reviews = get_text(soup, "a.-plxs._more")

    if not reviews:
        return None

    match = re.search(r"\d+", reviews)

    if not match:
        return None

    return match.group()

def get_rating(soup: BeautifulSoup) -> str | None:
    rating = get_text(soup, "div.stars")

    if not rating:
        return None

    rating_value = rating.split()[0]
    return rating_value


def parse_product_details(html: str) -> dict[str, Any]:
    """
    Extract structured product information from a Jumia product page.

    Args:
        html: HTML content of a product page.

    Returns:
        A dictionary containing the extracted product information.
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
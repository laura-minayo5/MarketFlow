from pathlib import Path
import json
import re
import uuid
import random
from utils.timestamps import generate_timestamp
from utils.ids import generate_product_id
from .inventory import parse_availability

"""
Hierarchy

Products
    │
    └── Product Categories
            │
            └── Categories
"""



def load_products(input_path: Path) -> list[dict]:
    """
    Load scraped products from a JSON file.
    Args:
        input_path: Path to products.json.
    Returns:
        A list of product dictionaries.
    """
    with input_path.open("r", encoding="utf-8") as f:
        # Read the JSON file and convert it into
        # a list of Python dictionaries.
        return json.load(f)


def clean_price(price: str | None) -> float | None:
    """
    Convert a price string into a float.
    Example: "KSh 2,470" -> 2470.0
    Returns None if the price is missing.
    """
    if not price:
        return None

    # Keep only digits and decimal points.
    numeric_price = re.sub(r"[^\d.]", "", price)

    return float(numeric_price)



def clean_discount(discount: str | None) -> int | None:
    """
    Convert a discount string into an integer percentage.
    Example: "35%" -> 35
    Returns None if the discount is missing.
    """
    if not discount:
        return None

    # Keep only digits.
    numeric_discount = re.sub(r"\D", "", discount)

    return int(numeric_discount)



def clean_rating(rating: str | None) -> float | None:
    """
    Convert a rating string into a float.
    Example:
        "4.5" -> 4.5
    Returns None if the rating is missing.
    """
    if not rating:
        return None

    return float(rating)



def clean_reviews(reviews: str | None) -> int | None:
    """
    Convert a reviews string into an integer.
    Example: "1,234" -> 1234
    Returns None if the reviews count is missing.
    """
    if not reviews:
        return None

    return int(reviews)


def enrich_product(product: dict) -> dict:
    """
    Enrich a scraped product with cleaned values and generated fields.
    """

    # Generate a unique identifier for the product.
    product_id = generate_product_id()

    # Convert the availability text into
    # a quantity and stock status.
    quantity_available, stock_status = parse_availability(
        product["availability"]
    )

    # Generate timestamps.
    timestamp = generate_timestamp()

    return {

        # Copy all original scraped fields.
        **product,

        # Generated identifier.
        "product_id": product_id,

        # Clean prices.
        "current_price": clean_price(product["current_price"]),
        "old_price": clean_price(product["old_price"]),
        "discount": clean_discount(product["discount"]),

        # Clean ratings.
        "rating": clean_rating(product["rating"]),
        "reviews": clean_reviews(product["reviews"]),

        # Inventory information.
        "quantity_available": quantity_available,
        "stock_status": stock_status,

        # Metadata.
        "created_at": timestamp,
        "updated_at": timestamp,
    }
import random
import re
from utils.id import generate_inventory_id


def parse_availability(availability: str | None) -> tuple[int, str]:
    """
    Convert scraped availability text into an inventory quantity
    and stock status.

    Examples:
        "In stock"       -> (20-100, "In Stock")
        "Few units left" -> (3-9, "Low Stock")
        "6 units left"   -> (6, "Low Stock")
        "Out of stock"   -> (0, "Out of Stock")

    Returns:
        (quantity_available, stock_status)
    """

    if not availability:
        return 0, "Unknown"

    availability = availability.lower()

    # Product is unavailable.
    if "out of stock" in availability:
        return 0, "Out of Stock"

    # Low stock but no exact quantity is provided.
    if "few" in availability:
        return random.randint(3, 9), "Low Stock"

    # Check whether an exact quantity is mentioned,
    # e.g. "6 units left".
    match = re.search(r"(\d+)", availability)

    if match:

        quantity = int(match.group(1))

        # Small quantities are considered low stock.
        if quantity <= 10:
            return quantity, "Low Stock"

        return quantity, "In Stock"

    # Product is simply marked as available.
    if "in stock" in availability:
        return random.randint(20, 100), "In Stock"

    # Fallback for unexpected wording.
    return 0, "Unknown"


def extract_inventory(products: list[dict]) -> list[dict]:
    """
    Create one inventory record for every product.

    The inventory information has already been calculated during
    product enrichment, so this function simply extracts the
    inventory-related fields into a separate inventory table.
    """

    inventory = []

    # Create one inventory record for every product.
    for product in products:

        inventory_record = {

            # Unique inventory identifier.
            "inventory_id": generate_inventory_id(),

            # Link inventory to the corresponding product.
            "product_id": product["product_id"],

            # Inventory values generated during enrichment.
            "quantity_available": product["quantity_available"],
            "stock_status": product["stock_status"],

            # Timestamp of the latest inventory update.
            "last_updated": product["updated_at"],
        }

        inventory.append(inventory_record)

    return inventory


def remove_inventory_fields(products: list[dict]) -> list[dict]:
    """
    Remove inventory-related fields from the enriched products.

    These fields belong in the inventory table and should not
    remain in the final products table.
    """

    cleaned_products = []

    # Process one product at a time.
    for product in products:

        # Copy the product so the original dictionary
        # is not modified.
        updated_product = product.copy()

        # Remove fields that belong to the inventory table.
        updated_product.pop("availability", None)
        updated_product.pop("quantity_available", None)
        updated_product.pop("stock_status", None)

        cleaned_products.append(updated_product)

    return cleaned_products
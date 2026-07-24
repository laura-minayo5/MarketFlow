from utils.ids import generate_seller_id


def extract_sellers(products: list[dict]) -> tuple[list[dict], dict]:
    """
    Extract unique sellers from products.

    Returns:
        sellers: list of seller records
        seller_lookup: seller name -> seller record
    """

    # Store unique sellers.
    seller_lookup = {}

    # Process one product at a time.
    for product in products:

        seller_name = product.get("seller")

        # Skip products without seller information.
        if not seller_name:
            continue

        # Skip sellers we've already processed.
        if seller_name in seller_lookup:
            continue

        # Retrieve the seller performance metrics.
        performance = product.get("seller_performance", {})

        # Create the seller record.
        seller = {
            "seller_id": generate_seller_id(),
            "seller_name": seller_name,
            "shipping_speed": performance.get("Shipping speed"),
            "quality_score": performance.get("Quality Score"),
            "customer_rating": performance.get("Customer Rating"),
            "cancellation_rate": performance.get("Cancellation Rate"),
        }

        # Save the seller using the seller name
        # as the lookup key.
        seller_lookup[seller_name] = seller

    return list(seller_lookup.values()), seller_lookup


def assign_seller_ids(products: list[dict], seller_lookup: dict) -> list[dict]:
    """
    Replace seller information with seller_id.
    """

    # Store the updated products.
    updated_products = []

    # Process one product at a time.
    for product in products:

        # Copy the product to avoid modifying
        # the original dictionary.
        updated_product = product.copy()

        seller_name = updated_product.get("seller")

        # Replace the seller name with its seller_id.
        if seller_name:
            updated_product["seller_id"] = (
                seller_lookup[seller_name]["seller_id"]
            )

        # Seller information is now stored in
        # the sellers table, so remove it
        # from the product.
        updated_product.pop("seller", None)
        updated_product.pop("seller_performance", None)

        updated_products.append(updated_product)

    return updated_products
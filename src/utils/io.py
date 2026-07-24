def get_tables(
    parsed_products: list[dict],
    product_tables: dict,
    customer_tables: dict,
    transaction_tables: dict,
) -> list[tuple[str, str, list[dict]]]:
    """
    Return all generated tables together with their filenames.
    """

    return [
        ("raw products", "parsed_products.json", parsed_products),
        ("enriched products", "enriched_products.json", product_tables["enriched_products"]),
        ("products", "products.json", product_tables["products"]),
        ("categories", "categories.json", product_tables["categories"]),
        ("sellers", "sellers.json", product_tables["sellers"]),
        ("inventory", "inventory.json", product_tables["inventory"]),
        ("customers", "customers.json", customer_tables["customers"]),
        ("addresses", "addresses.json", customer_tables["addresses"]),
        ("orders", "orders.json", transaction_tables["orders"]),
        ("order items", "order_items.json", transaction_tables["order_items"]),
        ("payments", "payments.json", transaction_tables["payments"]),
        ("reviews", "reviews.json", transaction_tables["reviews"]),
        ("wishlist", "wishlist.json", transaction_tables["wishlist"]),
        ("shopping carts", "shopping_carts.json", transaction_tables["shopping_carts"]),
    ]


def save_all_tables(
    tables: list[tuple[str, str, list[dict]]],
) -> None:
    """
    Save all generated tables.
    """

    for _, filename, data in tables:
        save_products(
            data,
            PROCESSED_DATA / filename,
        )


def print_all_summaries(
    tables: list[tuple[str, str, list[dict]]],
) -> None:
    """
    Print a summary of all saved tables.
    """

    for table_name, filename, data in tables:
        print_save_summary(
            table_name,
            data,
            PROCESSED_DATA / filename,
        )
"""
Hierarchy

Products
    │
    ▼
Product Categories
    ▲
    │
Categories
"""

def generate_product_categories(products: list[dict], category_lookup: dict) -> tuple[list[dict], list[dict]]:
    """
    Generate the product_categories bridge table.

    Returns:
        1. Products without breadcrumbs.
        2. Product-category relationships.
    """

    # Store cleaned products.
    updated_products = []

    # Store bridge table records.
    product_categories = []

    # Process one product at a time.
    for product in products:

        # Copy the product so the original dictionary
        # is not modified.
        updated_product = product.copy()

        # Retrieve the product breadcrumbs.
        # Skip the root "Home" category.
        breadcrumbs = updated_product.get("breadcrumbs", [])[1:]

        # Rebuild the full breadcrumb path.
        # Example:
        # "Electronics > Phones > Smartphones"
        path = ""

        # Create one bridge record for every
        # category in the breadcrumb path.
        # Rebuild the same breadcrumb path used during category extraction.
        # This path is the key used to find the correct category_id
        # in the category lookup dictionary.
        for category_name in breadcrumbs:

            # First iteration:
            # path = "Electronics"
            #
            # Second iteration:
            # path = "Electronics > Phones"
            #
            # Third iteration:
            # path = "Electronics > Phones > Smartphones"
            path = (
                f"{path} > {category_name}"
                if path
                else category_name
            )

            product_categories.append({

                # Link product to category.
                "product_id": updated_product["product_id"],
                "category_id": category_lookup[path]["category_id"],
            })

            
        # The breadcrumb has served its purpose,
        # so remove it from the product record.
        updated_product.pop("breadcrumbs", None)

        # Store the updated product. # Store the updated product.
        updated_products.append(updated_product)

    return updated_products, product_categories

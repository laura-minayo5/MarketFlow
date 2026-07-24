from utils.ids import generate_category_id

"""
Hierarchy

Categories
    │
    └── Product Categories
            │
            └── Products

Categories also form a hierarchy through:

Parent Category
        │
        ▼
Child Category
"""

def extract_categories(products: list[dict]) -> tuple[list[dict], dict]:
    """
    Extract unique categories from product breadcrumbs while
    preserving parent-child relationships.

    Returns:
        1. A list of category records for saving to categories.json.
        2. A lookup dictionary used to assign category IDs to products.
    """

    # Stores unique categories using their full breadcrumb path as the key.
    category_lookup = {}

    # Iterate through each product to extract its breadcrumb categories.
    for product in products:

        # Retrieve the product's breadcrumb trail and skip the root "Home" category.
        # The breadcrumbs is a list of category names, starting from the root category down to the specific category of the product.
        # "breadcrumbs": ["Home","Health & Beauty","Personal Hygiene","Skin Care","Body","Moisturizers","Lotions"]
        breadcrumbs = product.get("breadcrumbs", [])[1:]

        parent_id = None
        path = ""

        for category_name in breadcrumbs:

            # Build the full breadcrumb path.
            # Use the full breadcrumb path as the unique key.
            # This avoids duplicate names that may exist in different branches,
            # e.g. "Children" under Books vs Toys.
            path = (
                f"{path} > {category_name}"
                if path
                else category_name
            )

            # Skip categories we've already processed.
            if path in category_lookup:

                # The category already exists.
                # Reuse its category_id so that any child category
                # created next is linked to the correct parent.
                parent_id = category_lookup[path]["category_id"]
                continue

            category = {
                "category_id": generate_category_id(),
                "category_name": category_name,
                "parent_category_id": parent_id
            }

            category_lookup[path] = category

            # The category created in this iteration becomes the parent
            # of the next category in the breadcrumb path.
            parent_id = category["category_id"]

    # Return the list of unique categories and the dictionary of all categories.
    return list(category_lookup.values()), category_lookup


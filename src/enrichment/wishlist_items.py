import random
from utils.ids import generate_wishlist_item_id
from utils.timestamps import generate_timestamp

"""
Hierarchy

Wishlists
      │
      ▼
Wishlist Items
      │
      ▼
Products
"""

def generate_wishlist_items(wishlists: list[dict], products: list[dict]) -> list[dict]:
    """
    Generate wishlist items.

    Each wishlist contains between
    1 and 10 products.
    """

    # Store generated wishlist items.
    wishlist_items = []

    # Process one wishlist at a time.
    for wishlist in wishlists:

        # Decide how many products
        # are in this wishlist.
        number_of_products = random.randint(1, 10)

        # Select unique products.
        selected_products = random.sample(
            products,
            k=min(number_of_products, len(products))
        )

        # Create one wishlist item for each product.
        for product in selected_products:

            wishlist_item = {

                # Unique wishlist item identifier.
                "wishlist_item_id": generate_wishlist_item_id(),

                # Wishlist that contains the product.
                "wishlist_id": wishlist["wishlist_id"],

                # Product saved by the customer.
                "product_id": product["product_id"],

                # Date the product was added.
                "added_at": generate_timestamp(),
            }

            # Save the wishlist item.
            wishlist_items.append(wishlist_item)

    return wishlist_items
import random
from utils.ids import generate_wishlist_id
from utils.timestamps import generate_timestamp

"""
Hierarchy

Customers
    │
    ▼
Wishlists
    │
    ▼
Wishlist Items
"""

def generate_wishlists(customers: list[dict]) -> list[dict]:
    """
    Generate wishlists.

    Only some customers have wishlists.
    """

    # Store generated wishlists.
    wishlists = []

    # Process one customer at a time.
    for customer in customers:

        # About 40% of customers have wishlists.
        if random.random() > 0.4:
            continue

        # Generate timestamps.
        timestamp = generate_timestamp()

        wishlist = {

            # Unique wishlist identifier.
            "wishlist_id": generate_wishlist_id(),

            # Customer who owns the wishlist.
            "customer_id": customer["customer_id"],

            # Metadata timestamps.
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        # Save the wishlist.
        wishlists.append(wishlist)

    return wishlists
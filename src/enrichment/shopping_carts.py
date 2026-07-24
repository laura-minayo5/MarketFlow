import random
from utils.ids import generate_cart_id
from utils.timestamps import generate_timestamp

"""
Hierarchy

Customers
    │
    ▼
Shopping Carts
    │
    ▼
Cart Items
"""

def generate_shopping_carts(customers: list[dict]) -> list[dict]:
    """
    Generate shopping carts.

    Only some customers currently have active shopping carts.
    """

    # Store generated shopping carts.
    shopping_carts = []

    # Process one customer at a time.
    for customer in customers:

        # Simulate customer behaviour.
        # Only about 30% of customers currently
        # have an active shopping cart.
        if random.random() > 0.3:
            continue

        # Generate timestamps.
        timestamp = generate_timestamp()

        # Create the shopping cart.
        cart = {

            # Unique shopping cart identifier.
            "cart_id": generate_cart_id(),

            # Customer who owns the cart.
            "customer_id": customer["customer_id"],

            # Metadata timestamps.
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        # Save the shopping cart.
        shopping_carts.append(cart)

    return shopping_carts
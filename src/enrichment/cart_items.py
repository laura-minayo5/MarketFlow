import random
from utils.ids import generate_cart_item_id
from utils.timestamps import generate_timestamp

"""
Hierarchy

Shopping Carts
        │
        ▼
Cart Items
        │
        ▼
Products
"""

def generate_cart_items(shopping_carts: list[dict] products: list[dict]) -> list[dict]:
    """
    Generate items for every shopping cart.

    Each shopping cart contains between
    1 and 5 different products.
    """

    # Store generated cart items.
    cart_items = []

    # Process one shopping cart at a time.
    for cart in shopping_carts:

        # Decide how many products
        # are in this cart.
        number_of_products = random.randint(1, 5)

        # Select unique products.
        selected_products = random.sample(
            products,
            k=min(number_of_products, len(products))
        )

        # Create one cart item per product.
        for product in selected_products:

            quantity = random.randint(1, 3)

            cart_item = {

                # Unique cart item identifier.
                "cart_item_id": generate_cart_item_id(),

                # Shopping cart that owns this item.
                "cart_id": cart["cart_id"],

                # Product currently in the cart.
                "product_id": product["product_id"],

                # Quantity customer intends to purchase.
                "quantity": quantity,

                # Date product was added.
                "added_at": generate_timestamp(),
            }

            # Save the cart item.
            cart_items.append(cart_item)

    return cart_items
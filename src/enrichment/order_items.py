import random
from utils.ids import generate_order_item_id
  
"""
Hierarchy

Orders
    │
    ▼
Order Items
        │
        ▼
Products
"""

def generate_order_items(orders: list[dict], products: list[dict]) -> list[dict]:
    """
    Generate order items for every order.
    Each order contains between 1 and 5 products.
    """

    # Store all generated order items.
    order_items = []

    # Process one order at a time.
    for order in orders:

        # Randomly decide how many different products
        # this order will contain.
        number_of_products = random.randint(1, 5)

        # Randomly select products for this order.
        #
        # random.sample() ensures the same product
        # is not selected twice within one order.
        #
        # min() prevents requesting more products than
        # actually exist in the products list.
        selected_products = random.sample(
            products,
            k=min(number_of_products, len(products))
        )

        # Create one order item for every selected product.
        for product in selected_products:

            # Customer buys between 1 and 3 units
            # of the selected product.
            quantity = random.randint(1, 3)

            # Use the product's selling price
            # as the unit price.
            price = product["current_price"]

            # Calculate the total cost for this product
            # within the order.
            subtotal = price * quantity

            # Build the order item record.
            order_item = {
                "order_item_id": generate_order_item_id(),
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": price,
                "subtotal": subtotal,
            }

            # Save the generated order item.
            order_items.append(order_item)

    return order_items
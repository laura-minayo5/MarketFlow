import random
from utils.lookups import load_column
from utils.ids import generate_order_id
from utils.timestamps import generate_timestamp
"""
Hierarchy

Customers
    │
    ▼
Orders
    │
    ├── Order Items
    ├── Payments
    └── Shipments
"""

# Load possible order statuses from the lookup table.
ORDER_STATUSES = load_column("order_statuses.csv", "order_status")

# Load possible payment statuses from the lookup table.
PAYMENT_STATUSES = load_column("payment_statuses.csv", "payment_status")



def generate_orders(customers: list[dict], addresses: list[dict]) -> list[dict]:
    """
    Generate sythentic orders for customers.
    Each customer has between 1 and 5 orders.
    """

    orders = []

    # Quick lookup of customer -> address
    address_lookup = {
        address["customer_id"]: address["address_id"]
        for address in addresses
    }


    for customer in customers:

        number_of_orders = random.randint(1, 5)
        for _ in range(number_of_orders):

            # Select an order status using weighted probabilities.
            status = random.choices(
                ORDER_STATUSES,
                weights=[10, 10, 15, 60, 5],
            )[0]

            # Generate a timestamp for this order.
            timestamp = generate_timestamp()

            order = {
                "order_id": generate_order_id(),
                "customer_id": customer["customer_id"],
                "address_id": address_lookup[customer["customer_id"]],
                "order_status": status,
                "payment_status": random.choice(PAYMENT_STATUSES),

                # Newly created orders have not been updated yet,
                # so both timestamps are initially the same.
                "created_at": timestamp,
                "updated_at": timestamp,
            }

            orders.append(order)

    return orders

def update_order_totals(orders: list[dict], order_items: list[dict]) -> list[dict]:
    """
    Calculate the financial totals for every order based on
    the products contained in its order items.
    """

    # Build a lookup dictionary that groups order items
    # by their order_id.
    #
    # Example:
    # {
    #     "ORD001": [item1, item2],
    #     "ORD002": [item3],
    # }
    #
    # This lets us quickly retrieve all items belonging
    # to a specific order without repeatedly searching
    # through the entire order_items list.
    order_lookup = {}

    # Process one order item at a time.
    for item in order_items:

        order_id = item["order_id"]

        # If this order hasn't been seen before,
        # create an empty list to hold its items.
        if order_id not in order_lookup:
            order_lookup[order_id] = []

        # Add the current item to its corresponding order.
        order_lookup[order_id].append(item)

    # Store orders after their financial totals
    # have been calculated.
    updated_orders = []

    # Calculate totals for one order at a time.
    for order in orders:

        # Create a copy so the original order remains unchanged.
        updated_order = order.copy()

        # Retrieve every item belonging to this order.
        # If no items exist, return an empty list.
        items = order_lookup.get(order["order_id"], [])

        # Calculate the subtotal by adding together the
        # subtotal of every order item.
        subtotal = 0

        for item in items:
            subtotal += item["subtotal"]

        # subtotal = sum(item["subtotal"] for item in items)


        # Shipping is free for orders worth KSh 5,000 or more.
        # Otherwise, charge a flat shipping fee.
        shipping_cost = (0 if subtotal >= 5000 else 250)

        # Calculate VAT at 16%.
        tax_amount = round(subtotal * 0.16, 2)

        # Apply a 5% discount to large orders.
        discount_amount = (
            round(subtotal * 0.05, 2)
            if subtotal >= 10000
            else 0
        )

        # Calculate the final amount payable.
        total_amount = (
            subtotal
            + shipping_cost
            + tax_amount
            - discount_amount
        )

        # Add the calculated financial fields
        # to the copied order list(dict).
        updated_order.update({
            "subtotal": subtotal,
            "shipping_cost": shipping_cost,
            "tax_amount": tax_amount,
            "discount_amount": discount_amount,
            "total_amount": round(total_amount, 2),
        })

        # Save the updated order.
        updated_orders.append(updated_order)

    # Return the enriched orders containing
    # all financial totals.
    return updated_orders
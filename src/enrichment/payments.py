import random

from utils.lookups import load_column
from utils.ids import generate_payment_id

# Load available payment methods.
PAYMENT_METHODS = load_column("payment_methods.csv", "payment_method")


def generate_payments(orders: list[dict]) -> list[dict]:
    """
    Generate one payment record for every order.
    """

    # Store generated payment records.
    payments = []

    # Process one order at a time.
    for order in orders:

        # Customer only pays if the payment status is "Paid".
        amount_paid = (
            order["total_amount"]
            if order["payment_status"] == "Paid"
            else 0
        )

        # Build the payment record for this order.
        payment = {

            # Unique payment identifier.
            "payment_id": generate_payment_id(),

            # Link payment to its order.
            "order_id": order["order_id"],

            # Randomly choose a payment method.
            "payment_method": random.choice(PAYMENT_METHODS),

            # Reuse the payment status already assigned
            # to the order.
            "payment_status": order["payment_status"],
            
            # Customer only pays if the payment was successful.
            "amount_paid": amount_paid,

            # Assume payment is made when
            # the order is created.
            "payment_date": order["created_at"],
        }

        # Save the payment.
        payments.append(payment)

    return payments
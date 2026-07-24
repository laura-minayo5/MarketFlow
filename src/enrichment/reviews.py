import random
from utils.ids import generate_review_id
from utils.timestamps import generate_timestamp
from utils.lookups import load_column

# Load sample review comments.
REVIEW_COMMENTS = load_column(
    "review_comments.csv",
    "review_text",
)

def generate_reviews(
    orders: list[dict],
    order_items: list[dict],
) -> list[dict]:
    """
    Generate reviews only for purchased products.

    Not every purchased product receives a review.
    """

    reviews = []
    # Create a quick lookup so we can easily find
    # which customer placed a particular order.
    order_lookup = {
        order["order_id"]: order["customer_id"]
        for order in orders
    }

    # Process one purchased product at a time.
    for item in order_items:

        # Simulate customer behaviour.
        # Only about 40% of purchased products
        # receive reviews.
        if random.random() > 0.4:
            continue

        review = {

            # Unique review identifier.
            "review_id": generate_review_id(),

            # Retrieve the customer who purchased
            # this product using the order lookup.
            "customer_id": order_lookup[item["order_id"]],

            # Product being reviewed.
            "product_id": item["product_id"],

            # Generate a positive rating.
            "rating": random.randint(3, 5),

            # Random review text.
            "review_text": random.choice(REVIEW_COMMENTS),

            # Date the review was submitted.
            "review_date": generate_timestamp(),
        }

        reviews.append(review)

    return reviews
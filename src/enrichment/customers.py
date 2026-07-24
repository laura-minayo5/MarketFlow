import random
from faker import Faker
from utils.timestamps import generate_timestamp
from utils.ids import generate_customer_id

fake = Faker("en_KE")

EMAIL_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
]


def generate_customers(num_customers: int) -> list[dict]:
    """
    Generate synthetic customer records.

    Args:
        num_customers: Number of customer records to generate.

    Returns:
        A list of customer dictionaries.
    """

    customers = []

    # Generate the requested number of customers.
    for _ in range(num_customers):

        # Generate a random first and last name.
        first_name = fake.first_name()
        last_name = fake.last_name()

        # Create a username using the customer's name
        # and a random number to reduce duplicates.
        username = (
            f"{first_name.lower()}."
            f"{last_name.lower()}"
            f"{random.randint(10, 999)}"
        )

        # Generate a realistic account creation timestamp.
        created_at = generate_timestamp()

        customer = {
            "customer_id": generate_customer_id(),

            "first_name": first_name,
            "last_name": last_name,

            "username": username,

            # Generate an email address using the username
            # and a randomly selected email provider.
            "email": (
                f"{username}@"
                f"{random.choice(EMAIL_DOMAINS)}"
            ),

            # Generate a Kenyan phone number.
            "phone_number": fake.phone_number(),

            # Assign a random gender.
            "gender": random.choice(["Male", "Female"]),

            # Simulate that most customers are active.
            "is_active": random.choices(
                [True, False],
                weights=[95, 5],
            )[0],

            # Record when the customer account was created.
            "created_at": created_at,

            # Newly created accounts have not been updated yet,
            # so updated_at initially matches created_at.
            "updated_at": created_at,
        }

        customers.append(customer)

    return customers
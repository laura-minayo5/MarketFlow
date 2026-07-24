import csv
import random
import uuid
from utils.lookups import load_lookup
from utils.ids import generate_address_id


from faker import Faker

fake = Faker()

# Load locations from the lookup table.
# Each row in the CSV is a dictionary, so extract only the
# county, city, and postal code for address generation.
LOCATIONS = []

for row in load_lookup("locations.csv"):

    # Append a tuple containing the county, city and postal code.
    # Example:
    # ("Nairobi County", "Nairobi", "00100")
    LOCATIONS.append(
        (
            row["county"],
            row["city"],
            row["postal_code"],
        )
    )


def generate_addresses(customers: list[dict]) -> list[dict]:
    """
    Generate one Kenyan address for every customer.

    Returns:
        A list of customer address records.
    """

    # Store all generated customer addresses.
    addresses = []

    # Generate one address for each customer.
    for customer in customers:

        # Randomly select a valid Kenyan location from the seed data.
        # Example:
        # ("Nairobi County", "Nairobi", "00100")
        county, city, postal_code = random.choice(LOCATIONS)

        # Build the customer address record.
        address = {
            "address_id": generate_address_id(),
            "customer_id": customer["customer_id"],
            "street_address": fake.street_address(),
            "city": city,
            "county": county,
            "postal_code": postal_code,
            "country": "Kenya",
            "is_default": True,
            "created_at": customer["created_at"],
        }

        # Add the generated address to the list of addresses.
        addresses.append(address)
        
    return addresses
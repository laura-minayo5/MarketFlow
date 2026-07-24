from .enrich_products import enrich_product
from .categories import extract_categories, assign_category_ids
from .sellers import extract_sellers, assign_seller_ids
from .inventory import extract_inventory, remove_inventory_fields

from .customers import generate_customers
from .addresses import generate_addresses

from .orders import generate_orders, update_order_totals
from .order_items import generate_order_items
from .payments import generate_payments
from .reviews import generate_reviews
from .wishlist import generate_wishlist
from .shopping_carts import generate_shopping_carts


# product pipeline for MarketFlow.
def build_product_tables(raw_products: list[dict]) -> dict:
    """
    Build all product-related tables.
    """

    # First enrich every scraped product
    enriched_products = [
        enrich_product(product)
        for product in raw_products
    ]

    categories, category_lookup = extract_categories(enriched_products)
    products = assign_category_ids(enriched_products, category_lookup)

    sellers, seller_lookup = extract_sellers(products)
    products = assign_seller_ids(products, seller_lookup)

    inventory = extract_inventory(products)
    products = remove_inventory_fields(products)

    return {
        "enriched_products": enriched_products,
        "products": products,
        "categories": categories,
        "sellers": sellers,
        "inventory": inventory,
    }


# customer pipeline for MarketFlow.
def build_customer_tables(num_customers: int = 100):
    """
    Build all customer-related tables.
    """

    customers = generate_customers(num_customers)

    addresses = generate_addresses(customers)

    return {
        "customers": customers,
        "addresses": addresses,
    }


# order pipeline for MarketFlow.
def build_transaction_tables(
    customers,
    addresses,
    products,
):
    """
    Build all transactional tables.
    """

    orders = generate_orders(customers, addresses)

    order_items = generate_order_items(orders, products)

    orders = update_order_totals(orders, order_items)

    payments = generate_payments(orders)

    reviews = generate_reviews(orders, order_items)

    wishlist = generate_wishlist(customers, products)

    shopping_carts = generate_shopping_carts(customers, products)

    return {
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "reviews": reviews,
        "wishlist": wishlist,
        "shopping_carts": shopping_carts,
    }
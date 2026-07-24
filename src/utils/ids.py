import uuid

def generate_address_id() -> str:
    """
    Generate a unique address ID.
    """

    return f"ADD-{uuid.uuid4().hex[:8].upper()}"

def generate_category_id() -> str:
    """
    Generate a unique category ID.
    """

    return f"CAT-{uuid.uuid4().hex[:8].upper()}"

def generate_customer_id() -> str:
    """
    Generate a unique customer ID.
    """

    return f"CUS-{uuid.uuid4().hex[:8].upper()}"


def generate_product_id() -> str:
    """
    Generate a unique product ID.
    """

    return str(uuid.uuid4())


def generate_inventory_id() -> str:
    """
    Generate a unique inventory ID.
    """

    return f"INV-{uuid.uuid4().hex[:8].upper()}"


def generate_order_id() -> str:
    """
    Generate a unique order ID.
    """

    return f"ORD-{uuid.uuid4().hex[:8].upper()}"


def generate_order_item_id() -> str:
    """
    Generate a unique order item ID.
    """

    return f"ITEM-{uuid.uuid4().hex[:8].upper()}"


def generate_payment_id() -> str:
    """
    Generate a unique payment ID.
    """

    return f"PAY-{uuid.uuid4().hex[:8].upper()}"

def generate_review_id() -> str:
    """
    Generate a unique review ID.
    """

    return f"REV-{uuid.uuid4().hex[:8].upper()}"

def generate_seller_id() -> str:
    """
    Generate a unique seller ID.
    """

    return f"SEL-{uuid.uuid4().hex[:8].upper()}"


def generate_cart_id() -> str:
    """
    Generate a unique shopping cart ID.
    """

    return f"CART-{uuid.uuid4().hex[:8].upper()}"


def generate_cart_item_id() -> str:
    """
    Generate a unique shopping cart item ID.
    """

    return f"CITEM-{uuid.uuid4().hex[:8].upper()}"

def generate_wishlist_id() -> str:
    """
    Generate a unique wishlist ID.
    """

    return f"WISH-{uuid.uuid4().hex[:8].upper()}"


def generate_wishlist_item_id() -> str:
    """
    Generate a unique wishlist item ID.
    """

    return f"WITEM-{uuid.uuid4().hex[:8].upper()}"
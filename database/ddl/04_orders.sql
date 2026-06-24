-- (7 tables)

-- orders
-- order_items
-- payments
-- coupons
-- order_coupons

-- (plus references to lookup tables)

CREATE TABLE coupons (
    coupon_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    coupon_code VARCHAR(50) NOT NULL UNIQUE,
    discount_type VARCHAR(20) NOT NULL,
    discount_value NUMERIC(12,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    usage_limit INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_coupon_discount_type
        CHECK (discount_type IN ('PERCENTAGE','FIXED')),

    CONSTRAINT chk_coupon_discount_value
        CHECK (discount_value > 0),

    CONSTRAINT chk_coupon_dates
        CHECK (end_date >= start_date),

    CONSTRAINT chk_coupon_status
        CHECK (status IN ('ACTIVE','INACTIVE'))
);

CREATE TABLE orders (
    order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_status_id SMALLINT NOT NULL,

    subtotal_amount NUMERIC(12,2) NOT NULL,
    shipping_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    tax_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    total_amount NUMERIC(12,2) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_orders_status
        FOREIGN KEY (order_status_id)
        REFERENCES order_statuses(order_status_id),

    CONSTRAINT chk_order_amounts
        CHECK (
            subtotal_amount >= 0
            AND shipping_amount >= 0
            AND tax_amount >= 0
            AND discount_amount >= 0
            AND total_amount >= 0
        )
);

CREATE TABLE order_items (
    order_item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL,
    seller_product_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    line_total NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_order_items_seller_product
        FOREIGN KEY (seller_product_id)
        REFERENCES seller_products(seller_product_id),

    CONSTRAINT chk_order_item_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_order_item_prices
        CHECK (
            unit_price > 0
            AND discount_amount >= 0
            AND line_total >= 0
        )
);

CREATE TABLE payments (
    payment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL,
    payment_method_id SMALLINT NOT NULL,
    payment_status_id SMALLINT NOT NULL,

    amount NUMERIC(12,2) NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_reference VARCHAR(255),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_payments_method
        FOREIGN KEY (payment_method_id)
        REFERENCES payment_methods(payment_method_id),

    CONSTRAINT fk_payments_status
        FOREIGN KEY (payment_status_id)
        REFERENCES payment_statuses(payment_status_id),

    CONSTRAINT chk_payment_amount
        CHECK (amount > 0)
);

CREATE TABLE order_coupons (
    order_coupon_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    order_id BIGINT NOT NULL,
    coupon_id BIGINT NOT NULL,

    discount_amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_oc_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_oc_coupon
        FOREIGN KEY (coupon_id)
        REFERENCES coupons(coupon_id),

    CONSTRAINT chk_order_coupon_discount
        CHECK (discount_amount >= 0),

    CONSTRAINT uq_order_coupon
        UNIQUE(order_id, coupon_id)
);


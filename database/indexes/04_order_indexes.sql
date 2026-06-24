-- coupons
CREATE INDEX idx_coupons_status
ON coupons(status);

CREATE INDEX idx_coupons_start_date
ON coupons(start_date);

CREATE INDEX idx_coupons_end_date
ON coupons(end_date);

-- orders
CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_status
ON orders(order_status_id);

CREATE INDEX idx_orders_order_date
ON orders(order_date);

-- order_items
CREATE INDEX idx_order_items_order
ON order_items(order_id);

CREATE INDEX idx_order_items_seller_product
ON order_items(seller_product_id);

-- payments
CREATE INDEX idx_payments_order
ON payments(order_id);

CREATE INDEX idx_payments_method
ON payments(payment_method_id);

CREATE INDEX idx_payments_status
ON payments(payment_status_id);

CREATE INDEX idx_payments_date
ON payments(payment_date);

-- order_coupons
CREATE INDEX idx_order_coupons_order
ON order_coupons(order_id);

CREATE INDEX idx_order_coupons_coupon
ON order_coupons(coupon_id);
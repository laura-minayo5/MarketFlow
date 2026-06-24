-- ==========================================
-- MarketFlow Customer Domain Indexes
-- ==========================================

------------------------------------------------
-- customers
------------------------------------------------

-- Email already has a UNIQUE index

CREATE INDEX idx_customers_signup_date
ON customers(signup_date); --timebased index for queries on recent signups

CREATE INDEX idx_customers_status
ON customers(status); --index for queries on active/inactive customers

------------------------------------------------
-- customer_addresses
------------------------------------------------

CREATE INDEX idx_customer_addresses_customer
ON customer_addresses(customer_id); --index for queries on addresses by customer

CREATE INDEX idx_customer_addresses_city
ON customer_addresses(city); --index for queries on addresses by city

CREATE INDEX idx_customer_addresses_country
ON customer_addresses(country); --index for queries on addresses by country

------------------------------------------------
-- shopping_carts
------------------------------------------------

-- customer_id already has a UNIQUE index

CREATE INDEX idx_shopping_carts_created_at
ON shopping_carts(created_at); --timebased index for queries on recent carts

------------------------------------------------
-- cart_items
------------------------------------------------

CREATE INDEX idx_cart_items_cart
ON cart_items(cart_id); --index for queries on cart items by cart

CREATE INDEX idx_cart_items_seller_product
ON cart_items(seller_product_id); --index for queries on cart items by seller product

------------------------------------------------
-- wishlists
------------------------------------------------

-- customer_id already has a UNIQUE index

CREATE INDEX idx_wishlists_created_at
ON wishlists(created_at); --timebased index for queries on recent wishlists

------------------------------------------------
-- wishlist_items
------------------------------------------------

CREATE INDEX idx_wishlist_items_wishlist
ON wishlist_items(wishlist_id); --index for queries on wishlist items by wishlist

CREATE INDEX idx_wishlist_items_seller_product
ON wishlist_items(seller_product_id); --index for queries on wishlist items by seller product
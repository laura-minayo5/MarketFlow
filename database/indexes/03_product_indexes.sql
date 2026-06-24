-- sellers
CREATE INDEX idx_sellers_status
ON sellers(status);

-- products
CREATE INDEX idx_products_brand
ON products(brand);

CREATE INDEX idx_products_created_at
ON products(created_at);

-- categories
CREATE INDEX idx_categories_parent
ON categories(parent_category_id);

-- product_categories
CREATE INDEX idx_product_categories_category
ON product_categories(category_id);

-- seller_products
CREATE INDEX idx_seller_products_seller
ON seller_products(seller_id);

CREATE INDEX idx_seller_products_product
ON seller_products(product_id);

CREATE INDEX idx_seller_products_active
ON seller_products(active_flag);

-- inventory_movements
CREATE INDEX idx_inventory_movements_seller_product
ON inventory_movements(seller_product_id);

CREATE INDEX idx_inventory_movements_movement_type
ON inventory_movements(movement_type_id);

CREATE INDEX idx_inventory_movements_timestamp
ON inventory_movements(movement_timestamp);
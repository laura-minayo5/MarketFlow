-- (6 tables)
-- sellers
-- products
-- categories
-- product_categories
-- seller_products
-- inventory_movements

CREATE TABLE sellers (
    seller_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(30),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    seller_rating NUMERIC(3,2),
    joined_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_seller_status
        CHECK (status IN ('ACTIVE','INACTIVE')),

    CONSTRAINT chk_seller_rating
        CHECK (seller_rating BETWEEN 0 AND 5)
);

CREATE TABLE products (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    description TEXT,
    weight NUMERIC(10,2),
    dimensions VARCHAR(100),
    image_url TEXT,
    product_url TEXT,
    average_rating NUMERIC(3,2),
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_product_rating
        CHECK (average_rating BETWEEN 0 AND 5),

    CONSTRAINT chk_review_count
        CHECK (review_count >= 0)
);

CREATE TABLE categories (
    category_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    parent_category_id BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_categories_parent
        FOREIGN KEY (parent_category_id)
        REFERENCES categories(category_id)
);

CREATE TABLE product_categories (
    product_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,

    PRIMARY KEY (product_id, category_id),

    CONSTRAINT fk_pc_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_pc_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

CREATE TABLE seller_products (
    seller_product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    selling_price NUMERIC(12,2) NOT NULL,
    discount_price NUMERIC(12,2),
    currency VARCHAR(10) NOT NULL DEFAULT 'KES',
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sp_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id),

    CONSTRAINT fk_sp_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT chk_price_positive
        CHECK (selling_price > 0),

    CONSTRAINT chk_discount_price
        CHECK (
            discount_price IS NULL
            OR discount_price <= selling_price
        ),

    CONSTRAINT uq_seller_product
        UNIQUE (seller_id, product_id)
);

CREATE TABLE inventory_movements (
    movement_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_product_id BIGINT NOT NULL,
    movement_type_id SMALLINT NOT NULL,
    quantity INTEGER NOT NULL,
    reference_type VARCHAR(50),
    reference_id BIGINT,
    movement_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_im_seller_product
        FOREIGN KEY (seller_product_id)
        REFERENCES seller_products(seller_product_id),

    CONSTRAINT fk_im_movement_type
        FOREIGN KEY (movement_type_id)
        REFERENCES movement_types(movement_type_id),

    CONSTRAINT chk_inventory_quantity
        CHECK (quantity > 0)
);


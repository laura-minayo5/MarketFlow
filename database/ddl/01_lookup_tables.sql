-- (7 tables)

-- payment_methods
-- payment_statuses
-- order_statuses
-- shipment_statuses
-- return_statuses
-- return_reasons
-- movement_types


-- ==========================================
-- MarketFlow Lookup Tables
-- ==========================================

-- Payment Methods
CREATE TABLE payment_methods (
    payment_method_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    method_name VARCHAR(50) NOT NULL UNIQUE
);

-- Payment Statuses
CREATE TABLE payment_statuses (
    payment_status_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

-- Order Statuses
CREATE TABLE order_statuses (
    order_status_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

-- Shipment Statuses
CREATE TABLE shipment_statuses (
    shipment_status_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

-- Return Statuses
CREATE TABLE return_statuses (
    return_status_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

-- Return Reasons
CREATE TABLE return_reasons (
    return_reason_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reason_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Movement Types
CREATE TABLE movement_types (
    movement_type_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    movement_name VARCHAR(50) NOT NULL UNIQUE
);
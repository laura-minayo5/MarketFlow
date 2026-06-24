-- ==========================================
-- PAYMENT METHODS
-- ==========================================

INSERT INTO payment_methods (method_name)
VALUES
('MPESA'),
('VISA'),
('MASTERCARD'),
('PAYPAL'),
('BANK_TRANSFER');

-- ==========================================
-- PAYMENT STATUSES
-- ==========================================

INSERT INTO payment_statuses (status_name)
VALUES
('PENDING'),
('COMPLETED'),
('FAILED'),
('REFUNDED');

-- ==========================================
-- ORDER STATUSES
-- ==========================================

INSERT INTO order_statuses (status_name)
VALUES
('PENDING'),
('CONFIRMED'),
('SHIPPED'),
('DELIVERED'),
('CANCELLED');

-- ==========================================
-- SHIPMENT STATUSES
-- ==========================================

INSERT INTO shipment_statuses (status_name)
VALUES
('CREATED'),
('IN_TRANSIT'),
('OUT_FOR_DELIVERY'),
('DELIVERED'),
('CANCELLED');

-- ==========================================
-- RETURN STATUSES
-- ==========================================

INSERT INTO return_statuses (status_name)
VALUES
('REQUESTED'),
('APPROVED'),
('REJECTED'),
('REFUNDED');

-- ==========================================
-- RETURN REASONS
-- ==========================================

INSERT INTO return_reasons (
    reason_name,
    description
)
VALUES
('DAMAGED', 'Item damaged during shipping'),
('DEFECTIVE', 'Product not functioning properly'),
('WRONG_ITEM', 'Incorrect item received'),
('CHANGED_MIND', 'Customer no longer wants the item'),
('MISSING_PARTS', 'Product arrived incomplete'),
('SIZE_ISSUE', 'Product size not suitable');

-- ==========================================
-- MOVEMENT TYPES
-- ==========================================

INSERT INTO movement_types (movement_name)
VALUES
('STOCK_IN'),
('SALE'),
('RETURN'),
('DAMAGE'),
('ADJUSTMENT'),
('RESTOCK');
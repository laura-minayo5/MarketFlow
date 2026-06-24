-- (1 table)

-- returns

-- (return_statuses and return_reasons already exist)
CREATE TABLE returns (
    return_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_item_id BIGINT NOT NULL,
    return_reason_id SMALLINT NOT NULL,
    return_status_id SMALLINT NOT NULL,

    quantity_returned INTEGER NOT NULL,
    refund_amount NUMERIC(12,2) NOT NULL,

    return_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_returns_order_item
        FOREIGN KEY (order_item_id)
        REFERENCES order_items(order_item_id),

    CONSTRAINT fk_returns_reason
        FOREIGN KEY (return_reason_id)
        REFERENCES return_reasons(return_reason_id),

    CONSTRAINT fk_returns_status
        FOREIGN KEY (return_status_id)
        REFERENCES return_statuses(return_status_id),

    CONSTRAINT chk_quantity_returned
        CHECK (quantity_returned > 0),

    CONSTRAINT chk_refund_amount
        CHECK (refund_amount >= 0)
);
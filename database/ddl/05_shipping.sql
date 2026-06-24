-- (3 tables)

-- shipments
-- tracking_events

-- (shipment_statuses already exists)

CREATE TABLE shipments (
    shipment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL,
    shipment_status_id SMALLINT NOT NULL,
    carrier VARCHAR(100),
    tracking_number VARCHAR(255) UNIQUE,
    ship_date TIMESTAMP,
    estimated_delivery_date TIMESTAMP,
    actual_delivery_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_shipments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_shipments_status
        FOREIGN KEY (shipment_status_id)
        REFERENCES shipment_statuses(shipment_status_id),

    CONSTRAINT chk_delivery_dates
        CHECK (
            actual_delivery_date IS NULL
            OR actual_delivery_date >= ship_date
        )
);

CREATE TABLE tracking_events (
    tracking_event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    shipment_id BIGINT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tracking_events_shipment
        FOREIGN KEY (shipment_id)
        REFERENCES shipments(shipment_id)
);


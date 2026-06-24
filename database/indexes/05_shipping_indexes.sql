-- shipments

CREATE INDEX idx_shipments_order
ON shipments(order_id);

CREATE INDEX idx_shipments_status
ON shipments(shipment_status_id);

CREATE INDEX idx_shipments_ship_date
ON shipments(ship_date);

CREATE INDEX idx_shipments_actual_delivery_date
ON shipments(actual_delivery_date);

------------------------------------------------

-- tracking_events

CREATE INDEX idx_tracking_events_shipment
ON tracking_events(shipment_id);

CREATE INDEX idx_tracking_events_timestamp
ON tracking_events(event_timestamp);

CREATE INDEX idx_tracking_events_event_type
ON tracking_events(event_type);
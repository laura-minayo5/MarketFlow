-- returns

CREATE INDEX idx_returns_order_item
ON returns(order_item_id);

CREATE INDEX idx_returns_reason
ON returns(return_reason_id);

CREATE INDEX idx_returns_status
ON returns(return_status_id);

CREATE INDEX idx_returns_return_date
ON returns(return_date);

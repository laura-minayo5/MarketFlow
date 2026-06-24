-- reviews

CREATE INDEX idx_reviews_customer
ON reviews(customer_id);

CREATE INDEX idx_reviews_product
ON reviews(product_id);

CREATE INDEX idx_reviews_rating
ON reviews(rating);

CREATE INDEX idx_reviews_review_date
ON reviews(review_date);
DROP TABLE IF EXISTS sales_clean_base;

CREATE TABLE sales_clean_base (
    sale_id BIGSERIAL PRIMARY KEY,
    customer_id INT,
    product_id INT,
    sale_ts TIMESTAMP,
    quantity INT,
    amount NUMERIC(12,2),
    channel TEXT,
    currency TEXT,
    notes TEXT
);

INSERT INTO sales_clean_base (
    customer_id,
    product_id,
    sale_ts,
    quantity,
    amount,
    channel,
    currency,
    notes
)
SELECT
    (random()*200000)::INT + 1,
    (random()*5000)::INT + 1,
    NOW() - (random()*365 || ' days')::INTERVAL,
    (random()*5 + 1)::INT,
    round((random()*5000)::NUMERIC, 2),
    (ARRAY['online','store','app'])[floor(random()*3)+1],
    (ARRAY['USD','EUR','PKR'])[floor(random()*3)+1],
    NULL
FROM generate_series(1, 100000);


DROP TABLE IF EXISTS sales_dirty;
CREATE TABLE sales_dirty AS
SELECT * FROM sales_clean_base;

INSERT INTO sales_dirty
SELECT * FROM sales_clean_base
WHERE random() < 0.02;

UPDATE sales_dirty
SET customer_id = NULL
WHERE random() < 0.01;

UPDATE sales_dirty
SET quantity = -1
WHERE random() < 0.005;

UPDATE sales_dirty
SET amount = 999999
WHERE random() < 0.005;

UPDATE sales_dirty
SET sale_ts = NOW() + INTERVAL '10 days'
WHERE random() < 0.005;

UPDATE sales_dirty
SET channel = 'UNKNOWN'
WHERE random() < 0.01;


COPY sales_clean_base
TO 'G:/25280074_DE_Assignment_3/data/clean_synthetic_dataset.csv'
WITH CSV HEADER;

COPY sales_dirty
TO 'G:/25280074_DE_Assignment_3/data/corrupted_synthetic_dataset.csv'
WITH CSV HEADER;

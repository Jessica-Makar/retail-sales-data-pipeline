CREATE TABLE IF NOT EXISTS public.stg_customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32) NOT NULL,
    customer_zip_code_prefix VARCHAR(10) NOT NULL,
    customer_city VARCHAR(100) NOT NULL,
    customer_state VARCHAR(2) NOT NULL
);
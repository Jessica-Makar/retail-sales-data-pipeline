
CREATE TABLE IF NOT EXISTS public.stg_sellers (
    seller_id VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(10) NOT NULL,
    seller_city VARCHAR(100) NOT NULL,
    seller_state VARCHAR(2) NOT NULL
);

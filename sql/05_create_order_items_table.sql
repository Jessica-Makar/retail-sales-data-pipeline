
CREATE TABLE IF NOT EXISTS public.stg_order_items (
    order_id VARCHAR(32) NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id VARCHAR(32) NOT NULL,
    seller_id VARCHAR(32) NOT NULL,
    shipping_limit_date TIMESTAMP NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    freight_value NUMERIC(12, 2) NOT NULL,

    CONSTRAINT stg_order_items_pkey
        PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES public.stg_orders (order_id),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES public.stg_products (product_id),

    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_id)
        REFERENCES public.stg_sellers (seller_id)
);

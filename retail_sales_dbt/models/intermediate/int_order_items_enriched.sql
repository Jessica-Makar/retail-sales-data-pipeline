{{ config(materialized='view') }}

WITH order_items AS (
    SELECT *
    FROM {{ ref('stg_order_items') }}
),

products AS (
    SELECT *
    FROM {{ ref('stg_products') }}
),

sellers AS (
    SELECT *
    FROM {{ ref('stg_sellers') }}
)

SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    p.product_category_name,
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    oi.shipping_limit_date,
    oi.price,
    oi.freight_value

FROM order_items oi

LEFT JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
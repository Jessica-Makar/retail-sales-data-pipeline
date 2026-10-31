{{ config(materialized='table') }}

WITH customer_orders AS (
    SELECT *
    FROM {{ ref('int_customer_orders') }}
),

customer_summary AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS total_orders,
        MIN(order_purchase_timestamp) AS first_order_date,
        MAX(order_purchase_timestamp) AS most_recent_order_date
    FROM customer_orders
    GROUP BY customer_unique_id
)

SELECT
    customer_unique_id,
    total_orders,
    first_order_date,
    most_recent_order_date,
    most_recent_order_date::DATE - first_order_date::DATE
        AS days_between_first_and_most_recent_order,
    CASE
        WHEN total_orders > 1 THEN 'repeat'
        ELSE 'one_time'
    END AS customer_type
FROM customer_summary
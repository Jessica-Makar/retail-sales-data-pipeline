{{ config(materialized='table') }}

WITH delivered_orders AS (
    SELECT
        order_id,
        order_purchase_timestamp,
        total_payment_value
    FROM {{ ref('mart_orders') }}
    WHERE order_status = 'delivered'
      AND total_payment_value IS NOT NULL
),

monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_purchase_timestamp)::DATE
            AS order_month,
        COUNT(DISTINCT order_id) AS delivered_order_count,
        SUM(total_payment_value) AS total_sales,
        AVG(total_payment_value) AS average_order_value
    FROM delivered_orders
    GROUP BY DATE_TRUNC('month', order_purchase_timestamp)::DATE
)

SELECT
    order_month,
    delivered_order_count,
    total_sales,
    average_order_value
FROM monthly_sales
ORDER BY order_month
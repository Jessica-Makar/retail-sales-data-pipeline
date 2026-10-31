SELECT
    customer_unique_id,
    days_between_first_and_most_recent_order
FROM {{ ref('mart_customer_orders') }}
WHERE days_between_first_and_most_recent_order < 0
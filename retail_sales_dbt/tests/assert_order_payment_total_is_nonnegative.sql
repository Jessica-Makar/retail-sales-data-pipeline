SELECT
    order_id,
    total_payment_value
FROM {{ ref('int_order_payments') }}
WHERE total_payment_value < 0
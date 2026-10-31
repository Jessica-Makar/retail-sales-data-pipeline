SELECT
    payments.order_id
FROM {{ ref('int_order_payments') }} AS payments
LEFT JOIN {{ ref('int_customer_orders') }} AS orders
    ON payments.order_id = orders.order_id
WHERE orders.order_id IS NULL
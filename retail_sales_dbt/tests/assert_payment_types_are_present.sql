SELECT
    order_id,
    payment_types
FROM {{ ref('int_order_payments') }}
WHERE payment_types IS NULL
   OR TRIM(payment_types) = ''
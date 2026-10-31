SELECT
    order_id,
    payment_record_count
FROM {{ ref('int_order_payments') }}
WHERE payment_record_count <= 0
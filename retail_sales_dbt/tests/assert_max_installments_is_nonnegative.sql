SELECT
    order_id,
    max_installments
FROM {{ ref('int_order_payments') }}
WHERE max_installments < 0
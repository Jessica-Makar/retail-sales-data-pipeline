{{ config(materialized='view') }}

WITH payments AS (
    SELECT *
    FROM {{ ref('stg_payments') }}
)

SELECT
    order_id,

    SUM(payment_value) AS total_payment_value,
    
    COUNT(*) AS payment_record_count,
    
    MAX(payment_installments) AS max_installments,
    
    STRING_AGG(DISTINCT payment_type, ', ' ORDER BY payment_type) AS payment_types

FROM payments

GROUP BY order_id
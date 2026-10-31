SELECT
    order_id,
    review_count
FROM {{ ref('int_order_reviews') }}
WHERE review_count <= 0
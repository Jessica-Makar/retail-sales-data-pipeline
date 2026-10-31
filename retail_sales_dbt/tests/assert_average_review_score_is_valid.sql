SELECT
    order_id,
    average_review_score
FROM {{ ref('int_order_reviews') }}
WHERE average_review_score < 1
   OR average_review_score > 5
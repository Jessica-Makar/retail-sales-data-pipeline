SELECT
    reviews.order_id
FROM {{ ref('int_order_reviews') }} AS reviews
LEFT JOIN {{ ref('int_customer_orders') }} AS orders
    ON reviews.order_id = orders.order_id
WHERE orders.order_id IS NULL
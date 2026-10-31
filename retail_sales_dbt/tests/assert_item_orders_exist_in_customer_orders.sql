SELECT
    items.order_id
FROM {{ ref('int_order_items_enriched') }} AS items
LEFT JOIN {{ ref('int_customer_orders') }} AS orders
    ON items.order_id = orders.order_id
WHERE orders.order_id IS NULL
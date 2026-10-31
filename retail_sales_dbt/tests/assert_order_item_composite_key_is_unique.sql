SELECT
    order_id,
    order_item_id
FROM {{ ref('int_order_items_enriched') }}
GROUP BY
    order_id,
    order_item_id
HAVING COUNT(*) > 1
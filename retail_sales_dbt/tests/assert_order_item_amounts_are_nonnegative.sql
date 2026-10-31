SELECT
    order_id,
    order_item_id,
    price,
    freight_value
FROM {{ ref('int_order_items_enriched') }}
WHERE price < 0
   OR freight_value < 0
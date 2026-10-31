{{ config(materialized='table') }}

WITH customer_orders AS (
    SELECT *
    FROM {{ ref('int_customer_orders') }}
),

order_payments AS (
    SELECT *
    FROM {{ ref('int_order_payments') }}
),

order_reviews AS (
    SELECT *
    FROM {{ ref('int_order_reviews') }}
)

SELECT
    orders.order_id,
    orders.customer_unique_id,
    orders.customer_city,
    orders.customer_state,
    orders.order_status,
    orders.order_purchase_timestamp,
    orders.order_approved_at,
    orders.order_delivered_carrier_date,
    orders.order_delivered_customer_date,
    orders.order_estimated_delivery_date,

    payments.total_payment_value,
    payments.payment_record_count,
    payments.max_installments,
    payments.payment_types,

    reviews.review_count,
    reviews.average_review_score,
    reviews.min_review_score,
    reviews.max_review_score,
    reviews.latest_review_creation_date,
    reviews.latest_review_answer_timestamp

FROM customer_orders AS orders

LEFT JOIN order_payments AS payments
    ON orders.order_id = payments.order_id

LEFT JOIN order_reviews AS reviews
    ON orders.order_id = reviews.order_id
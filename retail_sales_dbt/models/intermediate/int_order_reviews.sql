{{ config(materialized='view') }}

WITH reviews AS (
    SELECT *
    FROM {{ ref('stg_reviews') }}
)

SELECT
    order_id,

    COUNT(*) AS review_count,

    ROUND(AVG(review_score)::NUMERIC, 2) AS average_review_score,

    MIN(review_score) AS min_review_score,

    MAX(review_score) AS max_review_score,

    MAX(review_creation_date) AS latest_review_creation_date,

    MAX(review_answer_timestamp) AS latest_review_answer_timestamp

FROM reviews

GROUP BY order_id
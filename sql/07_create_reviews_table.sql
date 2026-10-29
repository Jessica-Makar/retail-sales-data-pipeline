
CREATE TABLE IF NOT EXISTS public.stg_reviews (
    review_record_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    review_id VARCHAR(32) NOT NULL,
    order_id VARCHAR(32) NOT NULL,
    review_score INTEGER NOT NULL,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP NOT NULL,
    review_answer_timestamp TIMESTAMP NOT NULL,

    CONSTRAINT fk_reviews_order
        FOREIGN KEY (order_id)
        REFERENCES public.stg_orders (order_id),

    CONSTRAINT chk_reviews_score
        CHECK (review_score BETWEEN 1 AND 5)
);

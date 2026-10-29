
CREATE TABLE IF NOT EXISTS public.stg_payments (
    order_id VARCHAR(32) NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type VARCHAR(30) NOT NULL,
    payment_installments INTEGER NOT NULL,
    payment_value NUMERIC(12, 2) NOT NULL,

    CONSTRAINT stg_payments_pkey
        PRIMARY KEY (order_id, payment_sequential),

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES public.stg_orders (order_id),

    CONSTRAINT chk_payments_value_nonnegative
        CHECK (payment_value >= 0),

    CONSTRAINT chk_payments_installments_nonnegative
        CHECK (payment_installments >= 0)
);

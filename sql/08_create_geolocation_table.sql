
CREATE TABLE IF NOT EXISTS public.stg_geolocation (
    geolocation_record_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    geolocation_zip_code_prefix VARCHAR(5) NOT NULL,
    geolocation_lat NUMERIC(12, 8) NOT NULL,
    geolocation_lng NUMERIC(12, 8) NOT NULL,
    geolocation_city VARCHAR(100) NOT NULL,
    geolocation_state VARCHAR(2) NOT NULL,

    CONSTRAINT chk_geolocation_latitude
        CHECK (geolocation_lat BETWEEN -90 AND 90),

    CONSTRAINT chk_geolocation_longitude
        CHECK (geolocation_lng BETWEEN -180 AND 180)
);

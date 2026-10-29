from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"

load_dotenv(PROJECT_ROOT / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") or ""

database_url = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

timestamp_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def main():
    print("Reading orders CSV...")
    orders_df = pd.read_csv(DATA_FILE)

    print(f"Rows read: {len(orders_df):,}")

    print("Converting timestamp columns...")
    for column in timestamp_columns:
        orders_df[column] = pd.to_datetime(
            orders_df[column],
            errors="raise",
        )

    print("Loading orders into PostgreSQL...")
    engine = create_engine(database_url)

    try:
        orders_df.to_sql(
            name="stg_orders",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi",
        )
    finally:
        engine.dispose()

    print(f"Rows loaded: {len(orders_df):,}")
    print("Orders load completed successfully.")


if __name__ == "__main__":
    main()

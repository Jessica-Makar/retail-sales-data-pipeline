from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)

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


def main():
    print("Reading order-items CSV...")
    items_df = pd.read_csv(DATA_FILE)

    print(f"Rows read: {len(items_df):,}")

    print("Converting shipping timestamps...")
    items_df["shipping_limit_date"] = pd.to_datetime(
        items_df["shipping_limit_date"],
        errors="raise",
    )

    print("Checking composite key uniqueness...")
    if items_df.duplicated(
        subset=["order_id", "order_item_id"]
    ).any():
        raise ValueError(
            "Duplicate order_id + order_item_id combinations found. "
            "Load cancelled."
        )

    print("Checking monetary values...")
    if (items_df["price"] < 0).any():
        raise ValueError("Negative prices found. Load cancelled.")

    if (items_df["freight_value"] < 0).any():
        raise ValueError("Negative freight values found. Load cancelled.")

    engine = create_engine(database_url)

    try:
        
        print("Checking foreign-key references...")

        with engine.connect() as connection:
            existing_order_ids = set(
                connection.execute(
                    text("SELECT order_id FROM public.stg_orders")
                ).scalars().all()
            )

            existing_product_ids = set(
                connection.execute(
                    text("SELECT product_id FROM public.stg_products")
                ).scalars().all()
            )

            existing_seller_ids = set(
                connection.execute(
                    text("SELECT seller_id FROM public.stg_sellers")
                ).scalars().all()
            )

        unknown_orders = len(
            set(items_df["order_id"].unique()) - existing_order_ids
        )

        unknown_products = len(
            set(items_df["product_id"].unique()) - existing_product_ids
        )

        unknown_sellers = len(
            set(items_df["seller_id"].unique()) - existing_seller_ids
        )

        print(f"Unknown order IDs: {unknown_orders}")
        print(f"Unknown product IDs: {unknown_products}")
        print(f"Unknown seller IDs: {unknown_sellers}")

        if any([unknown_orders, unknown_products, unknown_sellers]):
            raise ValueError(
                "Foreign-key validation failed. Load cancelled."
            )


        print("Loading order items into PostgreSQL...")

        items_df.to_sql(
            name="stg_order_items",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=2000,
            method="multi",
        )

        print(f"Rows loaded: {len(items_df):,}")
        print("Order-items load completed successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()

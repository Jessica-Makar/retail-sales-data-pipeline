
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_products_dataset.csv"
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

integer_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]


def main():
    print("Reading products CSV...")
    products_df = pd.read_csv(DATA_FILE)

    print(f"Rows read: {len(products_df):,}")

    print("Converting numeric columns to nullable integers...")
    for column in integer_columns:
        products_df[column] = products_df[column].astype("Int64")

    print("Checking product ID uniqueness...")
    if products_df["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs found. Load cancelled.")

    print("Loading products into PostgreSQL...")
    engine = create_engine(database_url)

    try:
        products_df.to_sql(
            name="stg_products",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=2000,
            method="multi",
        )
    finally:
        engine.dispose()

    print(f"Rows loaded: {len(products_df):,}")
    print("Products load completed successfully.")


if __name__ == "__main__":
    main()

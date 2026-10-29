from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_sellers_dataset.csv"
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
    print("Reading sellers CSV...")
    sellers_df = pd.read_csv(
        DATA_FILE,
        dtype={"seller_zip_code_prefix": str},
    )

    print(f"Rows read: {len(sellers_df):,}")

    # Preserve postal-code prefixes as five-character strings.
    sellers_df["seller_zip_code_prefix"] = (
        sellers_df["seller_zip_code_prefix"].str.zfill(5)
    )

    print("Checking seller ID uniqueness...")
    if sellers_df["seller_id"].duplicated().any():
        raise ValueError("Duplicate seller IDs found. Load cancelled.")

    print("Loading sellers into PostgreSQL...")
    engine = create_engine(database_url)

    try:
        sellers_df.to_sql(
            name="stg_sellers",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=2000,
            method="multi",
        )
    finally:
        engine.dispose()

    print(f"Rows loaded: {len(sellers_df):,}")
    print("Sellers load completed successfully.")


if __name__ == "__main__":
    main()

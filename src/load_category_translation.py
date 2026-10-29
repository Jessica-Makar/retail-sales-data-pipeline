from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "product_category_name_translation.csv"
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
    print("Reading category translation CSV...")
    categories_df = pd.read_csv(DATA_FILE)

    print(f"Rows read: {len(categories_df):,}")

    print("Checking required fields...")
    if categories_df.isna().any().any():
        raise ValueError(
            "Missing values found. Load cancelled."
        )

    print("Checking Portuguese category uniqueness...")
    if categories_df["product_category_name"].duplicated().any():
        raise ValueError(
            "Duplicate Portuguese category names found. Load cancelled."
        )

    print("Checking English category uniqueness...")
    if categories_df["product_category_name_english"].duplicated().any():
        raise ValueError(
            "Duplicate English category names found. Load cancelled."
        )

    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            existing_rows = connection.execute(
                text(
                    "SELECT COUNT(*) "
                    "FROM public.stg_category_translation"
                )
            ).scalar_one()

        if existing_rows != 0:
            raise ValueError(
                "Destination table is not empty. Load cancelled."
            )

        print("Loading category translations into PostgreSQL...")

        categories_df.to_sql(
            name="stg_category_translation",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=1000,
            method="multi",
        )

        print(f"Rows loaded: {len(categories_df):,}")
        print("Category translation load completed successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()

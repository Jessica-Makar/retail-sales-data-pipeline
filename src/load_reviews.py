from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_reviews_dataset.csv"
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

timestamp_columns = [
    "review_creation_date",
    "review_answer_timestamp",
]


def main():
    print("Reading reviews CSV...")
    reviews_df = pd.read_csv(DATA_FILE)

    print(f"Rows read: {len(reviews_df):,}")

    print("Checking required fields...")
    required_columns = [
        "review_id",
        "order_id",
        "review_score",
        "review_creation_date",
        "review_answer_timestamp",
    ]

    if reviews_df[required_columns].isna().any().any():
        raise ValueError(
            "Missing values found in required fields. Load cancelled."
        )

    print("Checking review scores...")
    if not reviews_df["review_score"].between(1, 5).all():
        raise ValueError(
            "Review scores outside the 1-5 range found. Load cancelled."
        )

    print("Converting timestamps...")
    for column in timestamp_columns:
        reviews_df[column] = pd.to_datetime(
            reviews_df[column],
            errors="raise",
        )

    print("Checking order references...")
    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            existing_order_ids = set(
                connection.execute(
                    text("SELECT order_id FROM public.stg_orders")
                ).scalars().all()
            )

        unknown_orders = (
            set(reviews_df["order_id"].unique()) - existing_order_ids
        )

        print(f"Unknown order IDs: {len(unknown_orders)}")

        if unknown_orders:
            raise ValueError(
                "Unknown order IDs found. Load cancelled."
            )

        print("Loading reviews into PostgreSQL...")

        reviews_df.to_sql(
            name="stg_reviews",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=2000,
            method="multi",
        )

        print(f"Rows loaded: {len(reviews_df):,}")
        print("Reviews load completed successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()

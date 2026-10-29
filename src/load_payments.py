from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_payments_dataset.csv"
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
    print("Reading payments CSV...")
    payments_df = pd.read_csv(DATA_FILE)

    print(f"Rows read: {len(payments_df):,}")

    print("Checking required fields...")
    if payments_df.isna().any().any():
        raise ValueError("Missing values found. Load cancelled.")

    print("Checking payment key uniqueness...")
    if payments_df.duplicated(
        subset=["order_id", "payment_sequential"]
    ).any():
        raise ValueError(
            "Duplicate payment keys found. Load cancelled."
        )

    print("Checking payment values...")
    if (payments_df["payment_value"] < 0).any():
        raise ValueError("Negative payment values found. Load cancelled.")

    if (payments_df["payment_installments"] < 0).any():
        raise ValueError(
            "Negative installment counts found. Load cancelled."
        )

    print("Checking payment types...")
    print(payments_df["payment_type"].value_counts().to_dict())

    engine = create_engine(database_url)

    try:
        print("Checking order references...")

        with engine.connect() as connection:
            existing_order_ids = set(
                connection.execute(
                    text("SELECT order_id FROM public.stg_orders")
                ).scalars().all()
            )

        unknown_orders = (
            set(payments_df["order_id"].unique()) - existing_order_ids
        )

        print(f"Unknown order IDs: {len(unknown_orders)}")

        if unknown_orders:
            raise ValueError(
                "Unknown order IDs found. Load cancelled."
            )

        print("Loading payments into PostgreSQL...")

        payments_df.to_sql(
            name="stg_payments",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=2000,
            method="multi",
        )

        print(f"Rows loaded: {len(payments_df):,}")
        print("Payments load completed successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()

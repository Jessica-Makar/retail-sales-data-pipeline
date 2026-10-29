from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_geolocation_dataset.csv"
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

required_columns = [
    "geolocation_zip_code_prefix",
    "geolocation_lat",
    "geolocation_lng",
    "geolocation_city",
    "geolocation_state",
]


def main():
    print("Reading geolocation CSV...")
    geo_df = pd.read_csv(
        DATA_FILE,
        dtype={"geolocation_zip_code_prefix": str},
    )

    source_rows = len(geo_df)
    print(f"Source rows: {source_rows:,}")

    print("Checking required fields...")
    if geo_df[required_columns].isna().any().any():
        raise ValueError(
            "Missing values found in required fields. Load cancelled."
        )

    print("Checking coordinate ranges...")
    invalid_coordinates = (
        ~geo_df["geolocation_lat"].between(-90, 90)
        | ~geo_df["geolocation_lng"].between(-180, 180)
    )

    if invalid_coordinates.any():
        raise ValueError(
            "Coordinates outside valid global ranges. Load cancelled."
        )

    print("Identifying geographic outliers...")
    outside_brazil_box = ~(
        geo_df["geolocation_lat"].between(-34, 6)
        & geo_df["geolocation_lng"].between(-75, -32)
    )

    outlier_count = int(outside_brazil_box.sum())
    print(f"Rows outside broad Brazil bounds: {outlier_count:,}")

    print("Removing exact duplicate rows...")
    geo_df = geo_df.drop_duplicates(subset=required_columns).copy()

    removed_duplicates = source_rows - len(geo_df)
    print(f"Exact duplicate rows removed: {removed_duplicates:,}")
    print(f"Rows remaining: {len(geo_df):,}")

    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            existing_rows = connection.execute(
                text("SELECT COUNT(*) FROM public.stg_geolocation")
            ).scalar_one()

        if existing_rows != 0:
            raise ValueError(
                "Destination table is not empty. Load cancelled."
            )

        print("Loading geolocation data into PostgreSQL...")

        geo_df.to_sql(
            name="stg_geolocation",
            con=engine,
            schema="public",
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi",
        )

        print(f"Rows loaded: {len(geo_df):,}")
        print(f"Source rows: {source_rows:,}")
        print(f"Exact duplicates removed: {removed_duplicates:,}")
        print(f"Geographic outliers retained: {outlier_count:,}")
        print("Geolocation load completed successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()

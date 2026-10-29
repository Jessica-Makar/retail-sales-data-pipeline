from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "olist_geolocation_dataset.csv"
)


def main():
    print("Reading geolocation CSV...")
    geo_df = pd.read_csv(
        DATA_FILE,
        dtype={"geolocation_zip_code_prefix": str},
    )

    print("\n--- Dataset Overview ---")
    print(f"Rows: {len(geo_df):,}")
    print(f"Columns: {len(geo_df.columns)}")
    print(f"Column names: {list(geo_df.columns)}")

    print("\n--- First Five Rows ---")
    print(geo_df.head().to_string(index=False))

    print("\n--- Data Types ---")
    print(geo_df.dtypes)

    print("\n--- Missing Values ---")
    print(geo_df.isna().sum())

    print("\n--- Exact Duplicate Rows ---")
    print(f"Duplicate rows: {geo_df.duplicated().sum()}")

    print("\n--- Postal-Code Prefix Analysis ---")
    print(
        "Distinct postal-code prefixes: "
        f"{geo_df['geolocation_zip_code_prefix'].nunique():,}"
    )

    print(
        "Postal-code prefixes appearing more than once: "
        f"{(geo_df.groupby('geolocation_zip_code_prefix').size() > 1).sum():,}"
    )

    print(
        "Maximum rows for one postal-code prefix: "
        f"{geo_df.groupby('geolocation_zip_code_prefix').size().max():,}"
    )

    print("\n--- Coordinate Statistics ---")
    coordinate_columns = [
        "geolocation_lat",
        "geolocation_lng",
    ]

    print(geo_df[coordinate_columns].describe())

    print("\n--- Coordinate Range Checks ---")
    invalid_latitudes = ~geo_df["geolocation_lat"].between(-90, 90)
    invalid_longitudes = ~geo_df["geolocation_lng"].between(-180, 180)

    print(f"Invalid latitudes: {invalid_latitudes.sum():,}")
    print(f"Invalid longitudes: {invalid_longitudes.sum():,}")

    print("\n--- State Distribution ---")
    print(geo_df["geolocation_state"].value_counts().head(10))

    print("\n--- Postal-Code Prefix Lengths ---")
    print(
        geo_df["geolocation_zip_code_prefix"]
        .str.len()
        .value_counts()
        .sort_index()
    )


    print("\n--- Geographic Outlier Investigation ---")

    # Broad screening bounds for Brazil, not an exact national boundary.
    outside_brazil_box = ~(
        geo_df["geolocation_lat"].between(-34, 6)
        & geo_df["geolocation_lng"].between(-75, -32)
    )

    outliers = geo_df[outside_brazil_box]

    print(f"Rows outside broad Brazil bounds: {len(outliers):,}")

    print("\n--- First 20 Outlier Records ---")
    print(
        outliers[
            [
                "geolocation_zip_code_prefix",
                "geolocation_lat",
                "geolocation_lng",
                "geolocation_city",
                "geolocation_state",
            ]
        ].head(20).to_string(index=False)
    )

    print("\n--- Outliers by State ---")
    print(outliers["geolocation_state"].value_counts())

    print("\n--- Coordinate Range by State ---")
    print(
        geo_df.groupby("geolocation_state")[
            ["geolocation_lat", "geolocation_lng"]
        ].agg(["min", "max"]).to_string()
    )



if __name__ == "__main__":
    main()

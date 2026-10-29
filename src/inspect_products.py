from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_products_dataset.csv"
)

products_df = pd.read_csv(PRODUCTS_FILE)

print("=" * 50)
print("PRODUCTS DATASET INSPECTION")
print("=" * 50)

print(f"\nNumber of rows: {len(products_df):,}")
print(f"Number of columns: {len(products_df.columns)}")

print("\nColumn names:")
print(products_df.columns.tolist())

print("\nData types:")
print(products_df.dtypes)

print("\nMissing values per column:")
print(products_df.isna().sum())

print("\nDuplicate product IDs:")
print(products_df["product_id"].duplicated().sum())

print("\nAre product IDs unique?")
print(products_df["product_id"].is_unique)

print("\nFirst 5 rows:")
print(products_df.head().to_string(index=False))

print("\nMaximum string lengths:")
for column in [
    "product_id",
    "product_category_name",
]:
    print(f"{column}: {products_df[column].str.len().max()}")

print("\nProduct dimension statistics:")
dimension_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

print(products_df[dimension_columns].describe().round(2))

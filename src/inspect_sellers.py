
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SELLERS_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_sellers_dataset.csv"
)

sellers_df = pd.read_csv(SELLERS_FILE)

print("=" * 50)
print("SELLERS DATASET INSPECTION")
print("=" * 50)

print(f"\nNumber of rows: {len(sellers_df):,}")
print(f"Number of columns: {len(sellers_df.columns)}")

print("\nColumn names:")
print(sellers_df.columns.tolist())

print("\nData types:")
print(sellers_df.dtypes)

print("\nMissing values per column:")
print(sellers_df.isna().sum())

print("\nDuplicate seller IDs:")
print(sellers_df["seller_id"].duplicated().sum())

print("\nAre seller IDs unique?")
print(sellers_df["seller_id"].is_unique)

print("\nFirst 5 rows:")
print(sellers_df.head().to_string(index=False))

print("\nMaximum string lengths:")
for column in [
    "seller_id",
    "seller_city",
    "seller_state",
]:
    print(f"{column}: {sellers_df[column].str.len().max()}")

print("\nSeller counts by state:")
print(
    sellers_df["seller_state"]
    .value_counts()
    .head(10)
)

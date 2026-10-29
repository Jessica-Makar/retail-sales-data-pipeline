from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CUSTOMERS_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_customers_dataset.csv"
)

customers_df = pd.read_csv(CUSTOMERS_FILE)

print("=" * 50)
print("CUSTOMERS DATASET INSPECTION")
print("=" * 50)

print(f"\nNumber of rows: {len(customers_df):,}")
print(f"Number of columns: {len(customers_df.columns)}")

print("\nColumn names:")
print(customers_df.columns.tolist())

print("\nData types:")
print(customers_df.dtypes)

print("\nMissing values per column:")
print(customers_df.isna().sum())

print("\nDuplicate customer IDs:")
print(customers_df["customer_id"].duplicated().sum())

print("\nAre customer IDs unique?")
print(customers_df["customer_id"].is_unique)

print("\nFirst 5 rows:")
print(customers_df.head().to_string(index=False))

print("\nMaximum identifier and state lengths:")
for column in [
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state",
]:
    print(f"{column}: {customers_df[column].str.len().max()}")

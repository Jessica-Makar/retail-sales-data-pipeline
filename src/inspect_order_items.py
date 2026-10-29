from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ITEMS_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)

items_df = pd.read_csv(ITEMS_FILE)

print("=" * 50)
print("ORDER ITEMS DATASET INSPECTION")
print("=" * 50)

print(f"\nNumber of rows: {len(items_df):,}")
print(f"Number of columns: {len(items_df.columns)}")

print("\nColumn names:")
print(items_df.columns.tolist())

print("\nData types:")
print(items_df.dtypes)

print("\nMissing values per column:")
print(items_df.isna().sum())

print("\nDuplicate order_id + order_item_id combinations:")
print(
    items_df.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

print("\nUnique order IDs in order items:")
print(items_df["order_id"].nunique())

print("\nUnique product IDs in order items:")
print(items_df["product_id"].nunique())

print("\nUnique seller IDs in order items:")
print(items_df["seller_id"].nunique())

print("\nFirst 5 rows:")
print(items_df.head().to_string(index=False))

print("\nNumeric column statistics:")
print(
    items_df[["order_item_id", "price", "freight_value"]]
    .describe()
    .round(2)
)

print("\nOrder items per order:")
print(
    items_df.groupby("order_id")
    .size()
    .describe()
    .round(2)
)

print("\nMaximum identifier lengths:")
for column in ["order_id", "product_id", "seller_id"]:
    print(f"{column}: {items_df[column].str.len().max()}")

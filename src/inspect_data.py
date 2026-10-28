
from pathlib import Path

import pandas as pd


# Locating the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Locating the raw orders CSV file
orders_file = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"

# Loading the orders dataset
orders_df = pd.read_csv(orders_file)

# Display basic information
print("=" * 50)
print("ORDERS DATASET INSPECTION")
print("=" * 50)

print(f"\nNumber of rows: {len(orders_df):,}")
print(f"Number of columns: {len(orders_df.columns)}")

print("\nColumn names:")
print(orders_df.columns.tolist())

print("\nData types:")
print(orders_df.dtypes)

print("\nMissing values per column:")
print(orders_df.isna().sum())

print("\nFirst 5 rows:")
print(orders_df.head())


# Check for duplicate order IDs
duplicate_order_ids = orders_df["order_id"].duplicated().sum()

print("\nDuplicate order IDs:", duplicate_order_ids)

# Check whether every order ID is unique
print("Are all order IDs unique?", orders_df["order_id"].is_unique)



# Examine the distribution of order statuses
print("\nOrder status counts:")
print(orders_df["order_status"].value_counts(dropna=False))

# Examine missing timestamps by order status
date_columns = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
]

print("\nMissing timestamps by order status:")
print(
    orders_df.groupby("order_status")[date_columns]
    .agg(lambda column: column.isna().sum())
)


# Inspect delivered orders missing their customer delivery date
delivered_missing_date = orders_df[
    (orders_df["order_status"] == "delivered")
    & (orders_df["order_delivered_customer_date"].isna())
]

print("\nDelivered orders missing customer delivery date:")
print(delivered_missing_date.to_string(index=False))

print(
    "\nNumber of delivered orders missing customer delivery date:",
    len(delivered_missing_date),
)


# Check unique identifiers in the other datasets

customers_df = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "olist_customers_dataset.csv"
)

products_df = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "olist_products_dataset.csv"
)

sellers_df = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "olist_sellers_dataset.csv"
)

order_items_df = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)

print("\nUnique identifier checks:")

print(
    "Customers — duplicate customer_id:",
    customers_df["customer_id"].duplicated().sum(),
)

print(
    "Products — duplicate product_id:",
    products_df["product_id"].duplicated().sum(),
)

print(
    "Sellers — duplicate seller_id:",
    sellers_df["seller_id"].duplicated().sum(),
)

print(
    "Order items — duplicate order_id + order_item_id:",
    order_items_df.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum(),
)

print("\nColumn names Order Items:")
print(order_items_df.columns.tolist())


# Check relationships between datasets

print("\nRelationship checks:")

# Orders that reference unknown customers
unknown_customers = ~orders_df["customer_id"].isin(
    customers_df["customer_id"]
)

print(
    "Orders with unknown customer_id:",
    unknown_customers.sum(),
)

# Order items that reference unknown orders
unknown_orders = ~order_items_df["order_id"].isin(
    orders_df["order_id"]
)

print(
    "Order items with unknown order_id:",
    unknown_orders.sum(),
)

# Order items that reference unknown products
unknown_products = ~order_items_df["product_id"].isin(
    products_df["product_id"]
)

print(
    "Order items with unknown product_id:",
    unknown_products.sum(),
)

# Order items that reference unknown sellers
unknown_sellers = ~order_items_df["seller_id"].isin(
    sellers_df["seller_id"]
)

print(
    "Order items with unknown seller_id:",
    unknown_sellers.sum(),
)

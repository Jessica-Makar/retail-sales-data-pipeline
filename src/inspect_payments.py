from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "olist_order_payments_dataset.csv"
)


def main():
    print("Reading payments CSV...")
    payments_df = pd.read_csv(DATA_FILE)

    print("\n--- Dataset Overview ---")
    print(f"Rows: {len(payments_df):,}")
    print(f"Columns: {len(payments_df.columns)}")
    print(f"Column names: {list(payments_df.columns)}")

    print("\n--- First Five Rows ---")
    print(payments_df.head().to_string(index=False))

    print("\n--- Data Types ---")
    print(payments_df.dtypes)

    print("\n--- Missing Values ---")
    print(payments_df.isna().sum())

    print("\n--- Duplicate Rows ---")
    print(f"Exact duplicate rows: {payments_df.duplicated().sum()}")

    print("\n--- Payment Type Distribution ---")
    print(payments_df["payment_type"].value_counts(dropna=False))

    print("\n--- Payment Installments ---")
    print(payments_df["payment_installments"].describe())

    print("\n--- Payment Value Statistics ---")
    print(payments_df["payment_value"].describe())

    print("\n--- Order ID Uniqueness ---")
    print(f"Distinct order IDs: {payments_df['order_id'].nunique():,}")
    print(
        "Orders with multiple payment records: "
        f"{(payments_df.groupby('order_id').size() > 1).sum():,}"
    )

    print("\n--- Duplicate Order-Payment Combinations ---")
    print(
        "Duplicate (order_id, payment_sequential) combinations: "
        f"{payments_df.duplicated(subset=['order_id', 'payment_sequential']).sum():,}"
    )


if __name__ == "__main__":
    main()

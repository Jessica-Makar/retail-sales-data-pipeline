from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "product_category_name_translation.csv"
)


def main():
    print("Reading category translation CSV...")
    categories_df = pd.read_csv(DATA_FILE)

    print("\n--- Dataset Overview ---")
    print(f"Rows: {len(categories_df):,}")
    print(f"Columns: {len(categories_df.columns)}")
    print(f"Column names: {list(categories_df.columns)}")

    print("\n--- First 10 Rows ---")
    print(categories_df.head(10).to_string(index=False))

    print("\n--- Data Types ---")
    print(categories_df.dtypes)

    print("\n--- Missing Values ---")
    print(categories_df.isna().sum())

    print("\n--- Exact Duplicate Rows ---")
    print(f"Duplicate rows: {categories_df.duplicated().sum()}")

    print("\n--- Portuguese Category Uniqueness ---")
    print(
        "Distinct Portuguese categories: "
        f"{categories_df['product_category_name'].nunique():,}"
    )
    print(
        "Duplicate Portuguese categories: "
        f"{categories_df['product_category_name'].duplicated().sum():,}"
    )

    print("\n--- English Category Uniqueness ---")
    print(
        "Distinct English categories: "
        f"{categories_df['product_category_name_english'].nunique():,}"
    )
    print(
        "Duplicate English categories: "
        f"{categories_df['product_category_name_english'].duplicated().sum():,}"
    )

    print("\n--- String Lengths ---")
    for column in [
        "product_category_name",
        "product_category_name_english",
    ]:
        print(
            f"{column}: maximum length = "
            f"{categories_df[column].str.len().max()}"
        )


if __name__ == "__main__":
    main()

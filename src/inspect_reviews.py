from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "olist_order_reviews_dataset.csv"
)


def main():
    print("Reading reviews CSV...")
    reviews_df = pd.read_csv(DATA_FILE)

    print("\n--- Dataset Overview ---")
    print(f"Rows: {len(reviews_df):,}")
    print(f"Columns: {len(reviews_df.columns)}")
    print(f"Column names: {list(reviews_df.columns)}")

    print("\n--- First Five Rows ---")
    print(reviews_df.head().to_string(index=False))

    print("\n--- Data Types ---")
    print(reviews_df.dtypes)

    print("\n--- Missing Values ---")
    print(reviews_df.isna().sum())

    print("\n--- Exact Duplicate Rows ---")
    print(f"Duplicate rows: {reviews_df.duplicated().sum()}")

    print("\n--- Review Score Distribution ---")
    print(reviews_df["review_score"].value_counts().sort_index())

    print("\n--- Review Score Validation ---")
    invalid_scores = ~reviews_df["review_score"].between(1, 5)
    print(f"Scores outside 1-5: {invalid_scores.sum()}")

    print("\n--- Review ID Uniqueness ---")
    print(f"Distinct review IDs: {reviews_df['review_id'].nunique():,}")
    print(f"Duplicate review IDs: {reviews_df['review_id'].duplicated().sum():,}")

    print("\n--- Order ID Uniqueness ---")
    print(f"Distinct order IDs: {reviews_df['order_id'].nunique():,}")
    print(
        "Orders with multiple review records: "
        f"{(reviews_df.groupby('order_id').size() > 1).sum():,}"
    )

    print("\n--- Timestamp Columns ---")
    timestamp_columns = [
        "review_creation_date",
        "review_answer_timestamp",
    ]

    for column in timestamp_columns:
        parsed = pd.to_datetime(reviews_df[column], errors="coerce")
        print(f"{column}:")
        print(f"  Missing or unparseable: {parsed.isna().sum()}")
        print(f"  Earliest: {parsed.min()}")
        print(f"  Latest: {parsed.max()}")


    print("\n--- Duplicate Review ID Investigation ---")

    duplicate_reviews = reviews_df[
        reviews_df.duplicated(
            subset=["review_id"],
            keep=False,
        )
    ].sort_values("review_id")

    print(
        "Rows with a repeated review ID: "
        f"{len(duplicate_reviews):,}"
    )

    print(
        "Distinct repeated review IDs: "
        f"{duplicate_reviews['review_id'].nunique():,}"
    )

    print("\n--- First 10 Rows with Repeated Review IDs ---")
    print(
        duplicate_reviews[
            [
                "review_id",
                "order_id",
                "review_score",
                "review_comment_title",
                "review_comment_message",
                "review_creation_date",
                "review_answer_timestamp",
            ]
        ].head(10).to_string(index=False)
    )

    print("\n--- Are Repeated Review IDs Exact Duplicates? ---")
    repeated_rows = reviews_df[
        reviews_df.duplicated(
            subset=["review_id"],
            keep=False,
        )
    ]

    distinct_versions = repeated_rows.groupby("review_id").apply(
        lambda group: len(group.drop_duplicates()),
        include_groups=False,
    )

    print(
        "Repeated review IDs with identical rows: "
        f"{(distinct_versions == 1).sum():,}"
    )

    print(
        "Repeated review IDs with differing rows: "
        f"{(distinct_versions > 1).sum():,}"
    )


if __name__ == "__main__":
    main()

import pandas as pd


def test_order_ids_are_unique():
    orders = pd.DataFrame(
        {
            "order_id": ["order_1", "order_2", "order_3"],
        }
    )

    assert orders["order_id"].is_unique


def test_order_ids_are_not_null():
    orders = pd.DataFrame(
        {
            "order_id": ["order_1", "order_2", "order_3"],
        }
    )

    assert orders["order_id"].notna().all()
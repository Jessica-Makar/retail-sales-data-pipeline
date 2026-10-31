import pandas as pd


def validate_order_ids(orders: pd.DataFrame) -> bool:
    """
    Check that the dataset is not empty and that order IDs
    are present and unique.
    """
    if orders.empty:
        return False

    if orders["order_id"].isna().any():
        return False

    if not orders["order_id"].is_unique:
        return False

    return True


def test_valid_order_ids_pass():
    orders = pd.DataFrame(
        {
            "order_id": ["order_1", "order_2", "order_3"],
        }
    )

    assert validate_order_ids(orders) is True


def test_duplicate_order_ids_fail():
    orders = pd.DataFrame(
        {
            "order_id": ["order_1", "order_2", "order_2"],
        }
    )

    assert validate_order_ids(orders) is False


def test_missing_order_ids_fail():
    orders = pd.DataFrame(
        {
            "order_id": ["order_1", None, "order_3"],
        }
    )

    assert validate_order_ids(orders) is False


def test_empty_dataset_fails():
    orders = pd.DataFrame(
        {
            "order_id": [],
        }
    )

    assert validate_order_ids(orders) is False

# Data Quality Assessment

## 1. Dataset Overview

- Source: Brazilian E-Commerce Public Dataset by Olist
- Dataset inspected: Orders, customers, products, sellers, and order items
- Orders records: 99,441
- Orders columns: 8
- Raw CSV files: 9

## 2. Uniqueness Checks

The following identifiers were checked for duplicates:

| Dataset | Identifier | Duplicate Count |
|---|---|---:|
| Orders | order_id | 0 |
| Customers | customer_id | 0 |
| Products | product_id | 0 |
| Sellers | seller_id | 0 |
| Order items | order_id + order_item_id | 0 |

## 3. Relationship Checks

The following relationships were checked for unmatched identifiers:

| Relationship | Unmatched Count |
|---|---:|
| Orders to customers | 0 |
| Order items to orders | 0 |
| Order items to products | 0 |
| Order items to sellers | 0 |

## 4. Missing Timestamp Findings

The orders dataset contains missing values in these columns:

| Column | Missing Count |
|---|---:|
| order_approved_at | 160 |
| order_delivered_carrier_date | 1,783 |
| order_delivered_customer_date | 2,965 |

Missing timestamps vary by order status. Some missing delivery timestamps are expected for orders that have not reached delivery or were canceled.

Eight orders marked as delivered have no customer delivery timestamp. Seven have a carrier delivery timestamp, while one is missing both delivery timestamps.

These records will be preserved and flagged for investigation rather than assigned invented timestamps or automatically deleted.

## 5. Initial Conclusions

- The tested identifiers are unique in their respective datasets.
- The tested relationships contain no unmatched identifiers.
- Missing timestamps require status-aware validation.
- Additional data quality checks will be implemented in the pipeline.
- These findings describe the source data and do not yet represent automated production pipeline tests.

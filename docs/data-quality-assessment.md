
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


## PostgreSQL Loading Validation

### Orders Staging Table

Source file: `olist_orders_dataset.csv`

Destination table: `public.stg_orders`

- Rows loaded: 99,441
- Unique order IDs: 99,441
- Duplicate order IDs: 0
- Order status categories: 8
- Timestamp conversion: Successful
- Database row-count verification: Passed

### Validation Results

The loaded row count matches the source dataset. All order IDs are unique, and the order-status distribution matches the initial source-data inspection.

Missing timestamps were preserved as SQL NULL values rather than replaced with invented dates.


## Customer Data Loading Validation

### Customer Staging Table

Source file: `olist_customers_dataset.csv`

Destination table: `public.stg_customers`

- Rows loaded: 99,441
- Unique customer IDs: 99,441
- Duplicate customer IDs: 0
- Missing values in source: 0
- Postal-code prefixes stored as text
- Sampled postal-code prefixes verified as five characters
- Database row-count verification: Passed

### Validation Results

The loaded customer row count matches the source dataset. Customer IDs are unique, and postal-code prefixes preserve leading zeros. Customer state counts were queried successfully from PostgreSQL.


## Product Data Loading Validation

### Product Staging Table

Source file: `olist_products_dataset.csv`

Destination table: `public.stg_products`

- Rows loaded: 32,951
- Unique product IDs: 32,951
- Duplicate product IDs: 0
- Missing product categories: 610
- Missing product name lengths: 610
- Missing product weights: 2
- Missing product dimensions: 2 records
- Database row-count verification: Passed

### Validation Results

The loaded product row count matches the source dataset, and product IDs are unique. Missing categories and measurements were preserved as SQL NULL values rather than replaced with invented data.

Numeric attributes were converted to nullable integers before loading.


## Seller Data Loading Validation

### Seller Staging Table

Source file: `olist_sellers_dataset.csv`

Destination table: `public.stg_sellers`

- Rows loaded: 3,095
- Unique seller IDs: 3,095
- Duplicate seller IDs: 0
- Missing values in source: 0
- Postal-code prefixes stored as text
- Sampled postal-code prefixes verified as five characters
- Database row-count verification: Passed

### Validation Results

The loaded seller row count matches the source dataset. Seller IDs are unique, postal-code prefixes preserve leading zeros, and the seller state distribution matches the initial source-data inspection.


## Order Items Data Loading Validation

### Order Items Staging Table

Source file: `olist_order_items_dataset.csv`

Destination table: `public.stg_order_items`

- Rows loaded: 112,650
- Unique order-item combinations: 112,650
- Duplicate composite keys: 0
- Distinct orders represented: 98,666
- Distinct products represented: 32,951
- Distinct sellers represented: 3,095
- Missing values in source: 0
- Negative prices: 0
- Negative freight values: 0
- Unknown order IDs: 0
- Unknown product IDs: 0
- Unknown seller IDs: 0
- Timestamp conversion: Successful
- Database row-count verification: Passed

**Result:** All 112,650 order-item records were loaded successfully. Composite-key uniqueness, monetary-value checks, foreign-key references, and database row counts passed validation.


## Payments Data Loading Validation

### Payments Staging Table

Source file: `olist_order_payments_dataset.csv`

Destination table: `public.stg_payments`

- Rows loaded: 103,886
- Unique payment records: 103,886
- Duplicate composite keys: 0
- Distinct orders represented: 99,440
- Payment types: 5
- Missing values in source: 0
- Negative payment values: 0
- Negative installment counts: 0
- Unknown order IDs: 0
- Minimum payment value: 0.00
- Maximum payment value: 13,664.08
- Total payment value: 16,008,872.12
- Database row-count verification: Passed

**Result:** All 103,886 payment records were loaded successfully. Composite-key uniqueness, monetary-value checks, foreign-key references, and database row counts passed validation. Zero installment counts and the `not_defined` payment category were preserved for further investigation.


## Reviews Data Loading Validation

### Reviews Staging Table

Source file: `olist_order_reviews_dataset.csv`

Destination table: `public.stg_reviews`

- Rows loaded: 99,224
- Unique generated record IDs: 99,224
- Distinct source review IDs: 98,410
- Duplicate source review IDs: 814
- Distinct orders represented: 98,673
- Missing review titles: 87,656
- Missing review messages: 58,247
- Review score range: 1–5
- Invalid review scores: 0
- Unknown order IDs: 0
- Timestamp conversion: Successful
- Database row-count verification: Passed

**Result:** All 99,224 review records were loaded successfully. The generated primary key is unique, review scores are valid, order references passed validation, and missing comments and repeated source review IDs were preserved.


## Geolocation Data Loading Validation

### Geolocation Staging Table

Source file: `olist_geolocation_dataset.csv`

Destination table: `public.stg_geolocation`

- Source rows: 1,000,163
- Exact duplicate source rows removed: 261,831
- Rows loaded: 738,332
- Unique generated record IDs: 738,332
- Distinct postal-code prefixes: 19,015
- Missing values in source: 0
- Invalid global coordinate ranges: 0
- Source records outside broad Brazil screening bounds: 31
- Database records outside screening bounds after loading: 27
- Duplicate location combinations after loading: 5

**Precision finding:** The source data was deduplicated before loading. Coordinates were stored to eight decimal places, causing five pairs of distinct source records to become identical after rounding. This was confirmed by reproducing the rounding transformation in Python.

**Result:** All 738,332 deduplicated source records were loaded. Geographic outliers were retained for investigation, and coordinate precision effects were documented rather than silently removing additional records.


## Staging Data Load Validation

All nine source datasets were loaded into PostgreSQL staging tables and verified against their expected row counts.

| Staging table | Rows loaded |
|---|---:|
| `stg_orders` | 99,441 |
| `stg_customers` | 99,441 |
| `stg_products` | 32,951 |
| `stg_sellers` | 3,095 |
| `stg_order_items` | 112,650 |
| `stg_payments` | 103,886 |
| `stg_reviews` | 99,224 |
| `stg_geolocation` | 738,332 |
| `stg_category_translation` | 71 |
| **Total** | **1,289,091** |

### Validation approach

- Confirmed row counts for all nine staging tables.
- Validated primary-key uniqueness where applicable.
- Preserved missing values in optional source fields rather than filling them with invented values.
- Preserved repeated source review IDs by assigning a generated surrogate key to each review record.
- Preserved geographic outliers within valid global coordinate ranges and documented the geographic screening results.
- Removed exact duplicate geolocation source records before loading, reducing the geolocation dataset from 1,000,163 to 738,332 records.
- Used PostgreSQL constraints to enforce key relationships and selected data-quality rules.

### Outcome

All nine staging tables contain the expected number of records. The staging layer is ready for the next phase: developing and testing analytical data models.

**Note:** The row-count verification confirms that the expected number of records was loaded. Additional relationship, transformation, and business-logic tests will be performed during subsequent development.
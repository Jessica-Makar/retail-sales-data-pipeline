
# Retail Sales Data Pipeline

## Project Overview

This project builds an end-to-end data engineering pipeline using retail e-commerce data.

The pipeline will ingest raw data, clean and validate it with Python, store it in PostgreSQL, transform it into analytics-ready tables using dbt, and present business insights through Power BI.

## Project Goals

- Build a repeatable ETL pipeline using Python.
- Store and manage data using PostgreSQL and SQL.
- Transform data into fact and dimension tables using dbt.
- Implement data quality checks and error handling.
- Practice incremental data loading and safe pipeline reruns.
- Use AWS S3 for raw data storage.
- Create an interactive Power BI dashboard.
- Document the project and maintain it using Git and GitHub.

## Technology Stack

- Python
- SQL
- PostgreSQL
- dbt Core
- Docker
- AWS S3
- Power BI
- Git and GitHub

## Project Status

Planning and initial setup.

## Data Source

The project will use the Brazilian E-Commerce Public Dataset by Olist.

Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce


## Local Development Setup

### Technologies

- Python
- PostgreSQL 17
- SQLAlchemy
- psycopg
- python-dotenv
- pandas

### Database Configuration

The project uses a local PostgreSQL database named `retail_sales`.

Database connection settings are stored in a local `.env` file and are excluded from version control.

Required environment variables:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`


## Project Progress

- [x] Downloaded and inspected the Olist e-commerce dataset
- [x] Completed initial data-quality and relationship checks
- [x] Installed and started PostgreSQL locally
- [x] Created the `retail_sales` database
- [x] Verified the Python-to-PostgreSQL connection
- [x] Created nine PostgreSQL staging tables
- [x] Built Python loaders for all nine source datasets
- [x] Loaded and verified all nine staging tables
- [x] Documented data-quality findings and staging validation
- [ ] Build data transformations using dbt Core
- [ ] Develop data-quality and transformation tests
- [ ] Create reporting tables and analytical data models
- [ ] Build Power BI dashboards
- [ ] Containerize the pipeline with Docker
- [ ] Integrate AWS S3 for data storage

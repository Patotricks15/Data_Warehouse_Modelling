# Subscription Data Warehouse - SCD & Snowflake Schema

This is a study project designed to demonstrate the implementation of a **Snowflake Schema** and **Slowly Changing Dimensions (SCD) Type 2** using **DuckDB** and **Python**. It focuses on a subscription-based business model (like Netflix or Spotify), exploring advanced data warehousing techniques for history tracking and columnar optimization.

## Modeling: The Snowflake Schema

This project implements a Snowflake Schema, where dimensions are partially normalized to reduce redundancy and handle complex hierarchies.

### Dimension Tables
- **`dim_date`**: Time-related attributes for trend analysis.
- **`dim_users` (SCD Type 2)**: Tracks user profile changes over time. It uses `valid_from`, `valid_to`, and `is_current` to manage history.
- **`dim_plans`**: Subscription plans available for users.
- **`dim_plan_tiers` (Normalized)**: Specifically for the Snowflake structure, this table stores tier details (Basic, Standard, Premium) linked to `dim_plans`.

### Fact Table
- **`fact_subscriptions`**: Contains the history of monthly payments, linked to the **correct version** of the user at the time of payment.
    - Amount Paid
    - Discount Amount
    - Status (Active, Cancelled, etc.)

## Tech Stack

- **Database**: DuckDB (In-process OLAP database, optimized for columnar storage and analytical queries).
- **Language**: Python 3.x (Used for ETL simulation and data generation).
- **Libraries**: `duckdb`, `pandas` (For efficient data insertion), `random`, `datetime`.

## Project Structure

- `create_schema.sql`: SQL script containing the DDL for the Snowflake schema and SCD2 tables.
- `populate_dw.py`: Python script that simulates temporal data evolution, including region changes for users and monthly subscription generation.
- `subscription_dw.db`: The DuckDB database file (Created after running the script).
- `analysis_queries.sql`: A collection of SQL queries to explore the warehouse.

## How to Use

### 1. Requirements
Ensure you have Python installed. You will need to install the dependencies:
```bash
pip install duckdb pandas
```

### 2. Populate the Data
Run the population script. It will create the database, build the schema, and simulate 12 months of activity:
```bash
python populate_dw.py
```

### 3. Analyze the Data
You can use `dbeaver` or any DuckDB-compatible tool to run the queries found in `analysis_queries.sql`.

## Deep Dive & Interview Prep

### 1. Why use a Snowflake Schema for plans and tiers?
In a **Snowflake Schema**, we normalize dimensions (e.g., extracting tiers from plans). This reduces data redundancy and is useful when a sub-dimension (like `tiers`) is shared across multiple dimensions or has many attributes. While Star Schema is usually faster for joins, Snowflake is more organized for complex hierarchies and saves storage in very large datasets.

### 2. What is SCD Type 2 and why is it crucial for BI?
**Slowly Changing Dimension (SCD) Type 2** preserves historical data by creating a new record when an attribute changes. Without it, if a user moves from "North" to "South", all their past sales would incorrectly appear as "South" in reports. SCD2 allows us to answer: *"What was the revenue of the North region last year?"* accurately, even if those users aren't there anymore.

### 3. How does DuckDB differ from SQLite for Data Warehousing?
- **SQLite** is **Row-Oriented**: Great for "one record at a time" (OLTP), like a banking app.
- **DuckDB** is **Column-Oriented**: Great for "all records for one column" (OLAP), like calculating the `AVG` of 100 million rows. It uses **vectorized execution**, making analytical queries significantly faster than SQLite.

### 4. What is the role of the Surrogate Key in SCD Type 2?
In SCD Type 2, a single "Natural Key" (like `user_id = 101`) can have multiple rows in the dimension table. To link a specific version of a user to a fact, we use a **Surrogate Key** (`user_key`). The Fact Table stores the `user_key` that was active at the time of the event, ensuring perfect historical attribution.

### 5. What are the `valid_from` and `valid_to` columns?
These are **effective dating** columns. They define the lifespan of a record version. When joining a Fact Table with a point-in-time requirement, we look for a match where `fact.date` is between `dim.valid_from` and `dim.valid_to`.

---
*Created for advanced learning in Data Engineering, focusing on temporal data and OLAP optimization.*

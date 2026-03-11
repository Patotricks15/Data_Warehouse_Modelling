# Sales Data Warehouse - Study Project

This is a study project designed to demonstrate the implementation of a classic **Star Schema** Data Warehouse using **SQLite** and **Python**. It focuses on the sales domain, including dimensional modeling concepts and automated data population.

## Modeling: The Star Schema

The project implements a Star Schema with one central Fact table and four Dimension tables, optimized for analytical queries.

### Dimension Tables
- **`dim_date`**: Contains time-related attributes (day, month, year, quarter, weekday) to facilitate time-series analysis.
- **`dim_product`**: Stores product details including categories, subcategories, and brands.
- **`dim_customer`**: Holds customer demographic information like name, segment, and country.
- **`dim_store`**: Contains geographic information about the physical or digital stores.

### Fact Table
- **`fact_sales`**: The core of the warehouse, containing keys to all dimensions and quantitative measures:
    - Quantity
    - Unit Price
    - Discount
    - Total Revenue
    - Total Cost

## Tech Stack

- **Database**: SQLite (Portability and ease of use for study purposes).
- **Language**: Python 3.x (Used for data generation and database orchestration).
- **Libraries**: `sqlite3` (Standard library), `random`, `datetime`.

## Project Structure

- `create_schema.sql`: SQL script containing the DDL (Data Definition Language) to create the tables and indexes.
- `populate_dw.py`: Python script that generates and inserts synthetic data into the warehouse.
- `warehouse.db`: The SQLite database file containing the modeled data.

## How to Use

### 1. Requirements
Ensure you have Python installed on your system. No external libraries are required as it uses the standard library.

### 2. Initialize the Database (Optional)
If you wish to start from scratch, you can run the SQL script using a SQLite client or via command line:
```bash
sqlite3 warehouse.db < create_schema.sql
```

### 3. Populate the Data
Run the population script to generate 50,000 randomized sales records across 3 years of data:
```bash
python populate_dw.py
```


## Deep Dive & Interview Prep

### 1. Why choose a Star Schema over a Snowflake Schema for this project?
In a Modern Data Warehouse, **Star Schema** is generally preferred because it prioritizes **read performance** over storage efficiency. By denormalizing dimension tables (e.g., keeping `category` in `dim_product` instead of a separate `dim_category` table), we reduce the number of `JOIN` operations. In large-scale systems (BigQuery, Redshift, Snowflake), joins are expensive operations due to data shuffling. Star Schema simplifies the query execution plan for BI tools.

### 2. What is the role of Surrogate Keys (`*_key`) vs Natural Keys (`*_id`)?
**Surrogate Keys** (integers like `product_key`) are system-generated identifiers.
- **Independence:** They decouple the DW from source system changes (e.g., if a product ID changes in the ERP, the DW history remains intact).
- **Performance:** Integers are more efficient for indexing and joining than strings (Natural Keys), reduced storage footprint on the Fact table.
- **History Management:** Essential for implementing **SCD Type 2** (Slowly Changing Dimensions), where multiple rows can exist for the same Natural Key to track history.

### 3. How do B-Tree Indexes work under the hood and why use them on Foreign Keys?
SQLite (and most RDBMS) uses **B-Trees** (Balanced Trees) for indexing.
- **How it works:** It organizes data in a tree structure where leaf nodes contain pointers to actual rows. Lookups are $O(\log n)$, meaning searching 1 million rows takes only about 20 comparisons.
- **The Trade-off:**
    - **Pros:** Massive boost in `SELECT` performance during joins between `fact_sales` and dimensions.
    - **Cons:** Every `INSERT` or `UPDATE` on the Fact table triggers an index update, increasing I/O overhead. In a DW, we tolerate this because we usually perform **batch loads** and intensive **read analysis**.

### 4. Why are the indexes in the `fact_sales` table crucial?
In a Star Schema, almost every query filters by a dimension (e.g., "Give me revenue by category for the last month"). Without indexes on `date_key` or `product_key`, the engine would perform a **Full Table Scan**, reading every single row from disk. With 50,000 rows it's fast; with 500 million, it's impossible. Indexes allow the engine to "jump" directly to the relevant records.

### 5. How would you handle a customer changing their segment (SCD Type 2)?
If a customer moves from "Consumer" to "Corporate", we have two main options:
- **Type 1 (Overwrite):** Update the existing record. The history is lost (old sales will look like they were "Corporate").
- **Type 2 (History):** Add a new row to `dim_customer` with a new `customer_key` but the same `customer_id`. We add `effective_date` and `end_date` columns. This preserves the historical context of sales made while the customer was still a "Consumer".

---
*Created for learning purposes to explore Data Engineering and Business Intelligence concepts.*

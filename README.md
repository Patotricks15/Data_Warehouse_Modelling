# Data Warehouse Modelling Study 📊

This repository is dedicated to my practical learning journey in **Data Warehouse Modelling**. The goal is to evolve from simple dimensional implementations to complex architectures, documenting the design patterns and methodologies used to structure data for analytics.

## 🚀 Projects

Currently, the repository contains the following projects:

1. **[Sales Warehouse](./sales_warehouse)**: Fundamental implementation of a Star Schema for sales data.
    - **Focus**: Star Schema, Surrogate Keys, B-Tree Indexes, Python + SQLite.

2. **[Subscription Warehouse](./subscription_warehouse)**: Tracking user history with SCD Type 2 and Snowflake Schema.
    - **Focus**: SCD (Slowly Changing Dimensions) Type 2, Snowflake Schema, DuckDB (Columnar Storage).

---

## 🔝 Data Warehouse Modelling Concepts

This repository serves as a roadmap for mastering different data architecture styles and modelling techniques:

### 1. Dimensional Modelling (Kimball)
- **Star Schema**: Denormalized structure optimized for read performance and simplicity.
- **Snowflake Schema**: Normalized dimensional modelling for storage efficiency and data integrity.
- **Fact Table Types**: 
    - Transactional Facts (individual events).
    - Periodic Snapshots (status over time).
    - Accumulating Snapshots (processes with multiple milestones).
- **Dimension Types**: 
    - SCD (Slowly Changing Dimensions) Types 0, 1, 2, 3, 4, 6.
    - Role-Playing Dimensions (e.g., multiple dates in one fact).
    - Junk Dimensions (grouping miscellaneous flags).
    - Degenerate Dimensions (stored directly in the fact table).

### 2. Enterprise & Agile Modelling
- **Inmon Methodology**: The Corporate Information Factory (CIF) and 3NF modelling.
- **Data Vault 2.0**: Agile modelling for enterprise scale using Hubs, Links, and Satellites.
- **Anchor Modelling**: Highly normalized (6NF) modelling for extreme flexibility.

### 3. Advanced Design Patterns
- **Bridging Tables**: Handling many-to-many relationships.
- **Hierarchies**: Modelling parent-child relationships and ragged hierarchies.
- **Technical Keys**: Surrogate Keys vs Natural Keys vs Business Keys.
- **Semantic Layer**: Modelling definitions and metrics for end-user consumption.

### 4. Physical Modelling & Performance
- **Indexing Strategies**: B-Trees, Bitmap indexes, and their impact on query plans.
- **Partitioning & Clustering**: Organizing data physically to optimize massive scans.
- **Columnar Storage Impact**: How OLAP engines (Parquet, DuckDB) change modelling decisions compared to Row-based systems.
- **Vector Modelling**: Structuring unstructured data for AI-powered semantic search (RAG).

---

## 🛠️ Tech Stack in Focus
- **Modelling Specifications**: SQL (DDL), DBML.
- **Storage Engines**: SQLite (Row), PostgreSQL (Hybrid), DuckDB (Columnar).
- **Languages**: Python (for data generation and schema testing).

---

*This repository focuses on **how to structure data**, leaving transport and scheduling (ETL/Orchestration) to dedicated repositories.*

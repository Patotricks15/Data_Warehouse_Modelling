# Data Warehouse Modelling Study 📊

This repository is dedicated to my practical learning journey in data modelling for **Data Warehousing**. The goal is to evolve from simple implementations to complex architectures, documenting every step and concept learned along the way.

## 🚀 Projects

Currently, the repository contains the following projects:

1. **[Sales Warehouse](./sales_warehouse)**: Fundamental implementation of a Star Schema for sales data.
    - **Focus**: Star Schema, Surrogate Keys, B-Tree Indexes, Python + SQLite.

2. **[Subscription Warehouse](./subscription_warehouse)**: Tracking user history with SCD Type 2 and Snowflake Schema.
    - **Focus**: SCD (Slowly Changing Dimensions) Type 2, Snowflake Schema, DuckDB (Columnar Storage).

---

## 🔝 Learning Path & Concepts

Each new project in this repository aims to consolidate previous knowledge and introduce new challenges. The path is structured by complexity levels:

- **Dimensional Modelling**: Understanding Fact Tables and Dimension Tables.
- **Star Schema**: Denormalized structure optimized for read performance.
- **Technical Keys**: Use of Surrogate Keys vs Natural Keys for source system independence.
- **B-Tree Indexes**: Why and how to index Foreign Keys in the Fact Table.
- **Data Generation**: Creating Python scripts to simulate real-world business scenarios.
- **Reliability & Scalability Fundamentals**: Understanding how systems handle growth and failures (DDIA Part 1).
- **Snowflake Schema**: Normalized modelling when storage efficiency is a priority.
- **SCD (Slowly Changing Dimensions)**: Implementing history tracking (mainly Type 2).
- **Data Quality**: Monitoring dashboards and schema testing.
- **Incremental Loading**: ETL strategies to process only new data (Watermarking & Idempotency).
- **Column-Oriented Storage**: Deep dive into LSM-Trees vs B-Trees and why OLAP prefers columnar formats (Parquet, DuckDB).
- **Schema Evolution & Encoding**: Handling data changes using Avro, Parquet, or JSON Schema (DDIA Chapter 4).
- **ELT Techniques with dbt**: Transforming data within the Data Warehouse itself.
- **Data Vault 2.0**: Introduction to agile modelling with Hubs, Links, and Satellites.
- **Modern Data Stack Architecture**: Using Cloud tools (BigQuery, Snowflake, DuckDB).
- **Advanced Optimization**: Partitioning (Horizontal scaling), Clustering, and Sharding strategies.
- **Batch & Stream Processing**: Implementing Lambda/Kappa architectures and understanding "derived data" (DDIA Part 3).
- **CDC (Change Data Capture)**: Using logs to synchronize databases (Event-driven data integration).
- **Governance & Catalog**: Documenting and managing Data Lineage.
- **Real-time Analytics**: Integration with data streams (Kafka/Flink) for low-latency insights.
- **Consistency & Consensus**: Understanding distributed transactions and exactly-once processing.

---

## 🛠️ Tech Stack in Focus
- **Languages**: Python, SQL.
- **Databases**: SQLite, PostgreSQL, DuckDB.
- **ETL/ELT Tools**: dbt, Airflow (Future).

---
*This repository serves as a portfolio of technical evolution in Data Engineering.*

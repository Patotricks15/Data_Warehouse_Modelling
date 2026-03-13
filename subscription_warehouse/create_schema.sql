-- SCHEMA FOR SUBSCRIPTION WAREHOUSE (DUCKDB)
-- Focus: SCD Type 2 and Snowflake Schema

-- 1. Date Dimension (Simple)
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    quarter INTEGER,
    day_of_week STRING
);

-- 2. Snowflake Schema: Plan Tiers (Normalized Dimension)
CREATE TABLE dim_plan_tiers (
    tier_key INTEGER PRIMARY KEY,
    tier_name VARCHAR, -- 'Basic', 'Standard', 'Premium'
    max_screens INTEGER,
    resolution VARCHAR
);

-- 3. Plans Dimension (Points to dim_plan_tiers)
CREATE TABLE dim_plans (
    plan_key INTEGER PRIMARY KEY,
    plan_name VARCHAR,
    monthly_price DECIMAL(10,2),
    tier_key INTEGER,
    FOREIGN KEY (tier_key) REFERENCES dim_plan_tiers(tier_key)
);

-- 4. Users Dimension (SCD TYPE 2)
CREATE TABLE dim_users (
    user_key INTEGER PRIMARY KEY, -- Surrogate Key (SK)
    user_id INTEGER,              -- Natural Key (Source system ID)
    user_name VARCHAR,
    user_email VARCHAR,
    user_region VARCHAR,
    -- History Control Columns (SCD2)
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);

-- 5. Fact Table: Subscriptions
CREATE TABLE fact_subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    date_key INTEGER,
    user_key INTEGER, -- Foreign Key to the correct VERSION of the user (SK)
    plan_key INTEGER,
    amount_paid DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    status VARCHAR, -- 'Active', 'Cancelled', 'Refunded'
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (user_key) REFERENCES dim_users(user_key),
    FOREIGN KEY (plan_key) REFERENCES dim_plans(plan_key)
);

-- Indexes (In DuckDB, columnar storage already handles most optimizations,
-- but PKs and FKs help with integrity and joins)
CREATE INDEX idx_fact_date ON fact_subscriptions(date_key);
CREATE INDEX idx_fact_user ON fact_subscriptions(user_key);
CREATE INDEX idx_user_natural_id ON dim_users(user_id);

-- =========================
-- DIM DATE
-- =========================

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    day INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER,
    year INTEGER,
    weekday INTEGER,
    weekday_name TEXT,
    is_weekend INTEGER
);

-- =========================
-- DIM PRODUCT
-- =========================

CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    subcategory TEXT,
    brand TEXT
);

-- =========================
-- DIM CUSTOMER
-- =========================

CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT
);

-- =========================
-- DIM STORE
-- =========================

CREATE TABLE dim_store (
    store_key INTEGER PRIMARY KEY,
    store_name TEXT,
    city TEXT,
    state TEXT,
    country TEXT
);

-- =========================
-- FACT SALES
-- =========================

CREATE TABLE fact_sales (
    sale_key INTEGER PRIMARY KEY,

    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,

    quantity INTEGER,
    unit_price REAL,
    discount REAL,
    revenue REAL,
    cost REAL,

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

-- =========================
-- INDEXES (important for DW)
-- =========================

CREATE INDEX idx_sales_date
ON fact_sales(date_key);

CREATE INDEX idx_sales_product
ON fact_sales(product_key);

CREATE INDEX idx_sales_customer
ON fact_sales(customer_key);

CREATE INDEX idx_sales_store
ON fact_sales(store_key);
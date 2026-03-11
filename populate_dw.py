import sqlite3
import random
import datetime

conn = sqlite3.connect("warehouse.db")
cur = conn.cursor()

# ---------------------------
# DIM DATE
# ---------------------------

start_date = datetime.date(2022,1,1)
days = 365 * 3

month_names = [
"Jan","Feb","Mar","Apr","May","Jun",
"Jul","Aug","Sep","Oct","Nov","Dec"
]

weekday_names = [
"Mon","Tue","Wed","Thu","Fri","Sat","Sun"
]

date_keys = []

for i in range(days):

    d = start_date + datetime.timedelta(days=i)

    date_key = int(d.strftime("%Y%m%d"))
    date_keys.append(date_key)

    cur.execute("""
    INSERT INTO dim_date VALUES (?,?,?,?,?,?,?,?,?,?)
    """,(
        date_key,
        d.isoformat(),
        d.day,
        d.month,
        month_names[d.month-1],
        (d.month-1)//3 + 1,
        d.year,
        d.weekday(),
        weekday_names[d.weekday()],
        1 if d.weekday() >= 5 else 0
    ))

# ---------------------------
# DIM PRODUCT
# ---------------------------

categories = {
"Electronics":["Phone","Laptop","TV"],
"Clothing":["Shirt","Pants","Shoes"],
"Sports":["Ball","Bike","Fitness"],
"Home":["Furniture","Kitchen","Decor"]
}

brands = ["BrandA","BrandB","BrandC","BrandD"]

product_keys = []

pk = 1

for cat,subs in categories.items():

    for sub in subs:

        for i in range(10):

            product_keys.append(pk)

            cur.execute("""
            INSERT INTO dim_product VALUES (?,?,?,?,?,?)
            """,(
                pk,
                f"P{pk}",
                f"{sub} {pk}",
                cat,
                sub,
                random.choice(brands)
            ))

            pk += 1

# ---------------------------
# DIM CUSTOMER
# ---------------------------

segments = ["Consumer","Corporate","Small Business"]
countries = ["Brazil","USA","Germany","Canada"]

customer_keys = []

for i in range(1,501):

    customer_keys.append(i)

    cur.execute("""
    INSERT INTO dim_customer VALUES (?,?,?,?,?)
    """,(
        i,
        f"C{i}",
        f"Customer {i}",
        random.choice(segments),
        random.choice(countries)
    ))

# ---------------------------
# DIM STORE
# ---------------------------

cities = ["Sao Paulo","Rio","New York","Berlin","Toronto"]

store_keys = []

for i in range(1,21):

    store_keys.append(i)

    cur.execute("""
    INSERT INTO dim_store VALUES (?,?,?,?,?)
    """,(
        i,
        f"Store {i}",
        random.choice(cities),
        "State",
        "Country"
    ))

# ---------------------------
# FACT SALES
# ---------------------------

sales_rows = 50000

for i in range(1, sales_rows+1):

    quantity = random.randint(1,5)
    price = random.uniform(20,500)
    discount = random.uniform(0,0.25)

    revenue = quantity * price * (1-discount)
    cost = revenue * random.uniform(0.5,0.8)

    cur.execute("""
    INSERT INTO fact_sales VALUES (?,?,?,?,?,?,?,?,?,?)
    """,(
        i,
        random.choice(date_keys),
        random.choice(product_keys),
        random.choice(customer_keys),
        random.choice(store_keys),
        quantity,
        price,
        discount,
        revenue,
        cost
    ))

conn.commit()
conn.close()
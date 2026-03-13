import duckdb
import random
import pandas as pd
from datetime import datetime, timedelta

# Conectar ao DuckDB (cria o arquivo se não existir)
con = duckdb.connect('subscription_dw.db')

def setup_database():
    """Executes the SQL script to create tables"""
    with open('create_schema.sql', 'r') as f:
        sql = f.read()
    con.execute(sql)
    print("Database schema created.")

def populate_static_dimensions():
    # 1. Date Dimension
    start_date = datetime(2023, 1, 1)
    dates = []
    for i in range(730): # 2 years
        d = start_date + timedelta(days=i)
        dates.append({
            'date_key': int(d.strftime('%Y%m%d')),
            'full_date': d.date(),
            'day': d.day,
            'month': d.month,
            'year': d.year,
            'quarter': (d.month - 1) // 3 + 1,
            'day_of_week': d.strftime('%A')
        })
    df_dates = pd.DataFrame(dates)
    con.execute("INSERT INTO dim_date SELECT * FROM df_dates")

    # 2. Snowflake: Plan Tiers
    tiers = [
        (1, 'Basic', 1, '720p'),
        (2, 'Standard', 2, '1080p'),
        (3, 'Premium', 4, '4K')
    ]
    con.executemany("INSERT INTO dim_plan_tiers VALUES (?, ?, ?, ?)", tiers)

    # 3. Plans
    plans = [
        (1, 'Monthly Basic', 19.90, 1),
        (2, 'Monthly Standard', 39.90, 2),
        (3, 'Monthly Premium', 55.90, 3)
    ]
    con.executemany("INSERT INTO dim_plans VALUES (?, ?, ?, ?)", plans)
    print("Static dimensions populated.")

def populate_users_scd2():
    # Simulating temporal evolution for SCD2
    # Version 1 of 100 users in Jan 2023
    users_v1 = []
    for i in range(1, 101):
        users_v1.append((
            i, # key
            i, # id
            f"User {i}",
            f"user{i}@example.com",
            random.choice(['North', 'South', 'East', 'West']),
            datetime(2023, 1, 1),
            None,
            True
        ))
    con.executemany("INSERT INTO dim_users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", users_v1)

    # Version 2: 20 users changed region in July 2023
    changed_users = random.sample(range(1, 101), 20)
    for user_id in changed_users:
        # 1. Expire old record
        con.execute(f"""
            UPDATE dim_users 
            SET valid_to = ?, is_current = False 
            WHERE user_id = ? AND is_current = True
        """, (datetime(2023, 7, 1), user_id))
        
        # 2. Insert new record (New Surrogate Key 100 + i)
        con.execute(f"""
            INSERT INTO dim_users (user_key, user_id, user_name, user_email, user_region, valid_from, is_current)
            SELECT 100 + {user_id}, user_id, user_name, user_email, 'New Region', ?, True
            FROM dim_users WHERE user_id = {user_id} AND valid_to = ?
        """, (datetime(2023, 7, 1), datetime(2023, 7, 1)))
    
    print("Users with SCD Type 2 history populated.")

def populate_facts():
    # Generate monthly subscriptions
    plans = con.execute("SELECT plan_key FROM dim_plans").fetchall()
    
    fact_id = 1
    for month in range(1, 13): # 12 months of 2023
        date_key = int(f"2023{month:02d}01")
        
        # For each month, we get the users ACTIVE at that time
        current_date = datetime(2023, month, 1)
        users = con.execute("""
            SELECT user_key FROM dim_users 
            WHERE ? >= valid_from AND (? < valid_to OR valid_to IS NULL)
        """, (current_date, current_date)).fetchall()
        
        subscriptions = []
        for user in users:
            plan = random.choice(plans)[0]
            price = con.execute(f"SELECT monthly_price FROM dim_plans WHERE plan_key = {plan}").fetchone()[0]
            
            subscriptions.append((
                fact_id,
                date_key,
                user[0],
                plan,
                price,
                0.0,
                'Active'
            ))
            fact_id += 1
            
        con.executemany("INSERT INTO fact_subscriptions VALUES (?, ?, ?, ?, ?, ?, ?)", subscriptions)
    
    print(f"Fact table populated with {fact_id - 1} records.")

if __name__ == "__main__":
    try:
        setup_database()
        populate_static_dimensions()
        populate_users_scd2()
        populate_facts()
        print("\nSuccess! The subscription DW was created and populated.")
        print("File generated: subscription_dw.db")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

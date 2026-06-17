import sqlite3
import pandas as pd
import os
 
def initialize_database():
    BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH    = os.path.join(BASE_DIR, "database", "food_wastage.db")
    DATA_DIR   = os.path.join(BASE_DIR, "data")
    DB_DIR     = os.path.join(BASE_DIR, "database")
 
    # Create database folder if it doesn't exist
    os.makedirs(DB_DIR, exist_ok=True)
 
    # Only create if database doesn't exist
    if not os.path.exists(DB_PATH):
        print("Database not found — creating fresh database...")
 
        conn = sqlite3.connect(DB_PATH)
 
        # Load CSVs
        providers     = pd.read_csv(os.path.join(DATA_DIR, "providers_data.csv"))
        receivers     = pd.read_csv(os.path.join(DATA_DIR, "receivers_data.csv"))
        food_listings = pd.read_csv(os.path.join(DATA_DIR, "food_listings_data.csv"))
        claims        = pd.read_csv(os.path.join(DATA_DIR, "claims_data.csv"))
 
        # Clean column names
        for df in [providers, receivers, food_listings, claims]:
            df.columns = df.columns.str.strip()
 
        # Write to SQLite
        providers.to_sql("providers",         conn, if_exists="replace", index=False)
        receivers.to_sql("receivers",         conn, if_exists="replace", index=False)
        food_listings.to_sql("food_listings", conn, if_exists="replace", index=False)
        claims.to_sql("claims",               conn, if_exists="replace", index=False)
 
        conn.commit()
        conn.close()
        print("Database created successfully!")
    else:
        print("Database already exists — skipping setup.")
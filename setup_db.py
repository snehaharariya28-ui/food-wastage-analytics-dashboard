import sqlite3
import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "database", "food_wastage.db")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Connect to SQLite 
conn = sqlite3.connect(DB_PATH)
print(f"Connected to database: {DB_PATH}")

# Load CSVs into pandas DataFrames 
providers     = pd.read_csv(os.path.join(DATA_DIR, "providers_data.csv"))
receivers     = pd.read_csv(os.path.join(DATA_DIR, "receivers_data.csv"))
food_listings = pd.read_csv(os.path.join(DATA_DIR, "food_listings_data.csv"))
claims        = pd.read_csv(os.path.join(DATA_DIR, "claims_data.csv"))

# Strip accidental whitespace from column names
for df in [providers, receivers, food_listings, claims]:
    df.columns = df.columns.str.strip()

# Write DataFrames to SQLite tables 
providers.to_sql("providers",         conn, if_exists="replace", index=False)
receivers.to_sql("receivers",         conn, if_exists="replace", index=False)
food_listings.to_sql("food_listings", conn, if_exists="replace", index=False)
claims.to_sql("claims",               conn, if_exists="replace", index=False)

print("All 4 tables loaded successfully!")

# Verify 
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables in database: {[t[0] for t in tables]}")

# Close connection 
conn.commit()
conn.close()
print("Database setup complete! Now run the Streamlit app.")


import pandas as pd
import sqlite3
import os

current_dir = os.path.dirname(__file__)

df = pd.read_csv(os.path.join(current_dir, "..", "data", "retail_sales_cleaned.csv"))

conn = sqlite3.connect(os.path.join(current_dir, "..", "sql", "retail_sales.db"))

df.to_sql("retail_sales", conn, if_exists="replace", index=False)

conn.close()

print("Database created!")

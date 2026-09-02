import pandas as pd
import sqlite3

df = pd.read_csv("data/retail_sales_cleaned.csv")

conn = sqlite3.connect("sql/retail_sales.db")

df.to_sql("retail_sales", conn, if_exists="replace", index=False)

conn.close()

print("Database created!")
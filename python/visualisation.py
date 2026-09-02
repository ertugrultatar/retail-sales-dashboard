import pandas as pd
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(__file__)

df = pd.read_csv(
    os.path.join(current_dir, "..", "data", "retail_sales_cleaned.csv")
)

df["order_date"] = pd.to_datetime(df["order_date"])


# 1. Yearly Sales
yearly_sales = (
    df.groupby(df["order_date"].dt.to_period("Y"))["sales_amount"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(8,5))

plt.bar(
    yearly_sales["order_date"].astype(str),
    yearly_sales["sales_amount"]
)

plt.title("Yearly Sales")
plt.xlabel("Year")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()





# 2. Sales by Category
sales_by_category = (
    df.groupby("product_category")["sales_amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(8,5))

plt.bar(
    sales_by_category["product_category"],
    sales_by_category["sales_amount"]
)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()




# 3. Top Products
top_products = (
    df.groupby(["product_name","product_category"])["sales_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
plt.figure(figsize=(10,5))

plt.bar(
    top_products["product_name"],
    top_products["sales_amount"]
)

plt.title("Top 10 Products")
plt.xlabel("Product")
plt.ylabel("Sales")

plt.xticks(rotation=90)
plt.tight_layout()




# Show all charts
plt.show()
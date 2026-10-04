import matplotlib

matplotlib.use("Agg")  # save charts to files without opening windows

import matplotlib.pyplot as plt
import os

from analysis import df, monthly_sales, yearly_sales, sales_by_category, top_products

current_dir = os.path.dirname(__file__)
images_dir = os.path.join(current_dir, "..", "images")


def save_chart(filename):

    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, filename), dpi=150)
    plt.close()
    print(f"Saved images/{filename}")


# 1. Yearly Sales
yearly = yearly_sales(df)

plt.figure(figsize=(8,5))

plt.bar(
    yearly["order_date"].astype(str),
    yearly["sales_amount"]
)

plt.title("Yearly Sales")
plt.xlabel("Year")
plt.ylabel("Sales (₹)")

save_chart("yearly_sales.png")


# 2. Monthly Sales vs Profit (chronological, not combined across years)
monthly = monthly_sales(df)
months = monthly["order_date"].dt.to_timestamp()

plt.figure(figsize=(12,5))

plt.plot(months, monthly["sales_amount"], label="Sales")
plt.plot(months, monthly["profit"], label="Profit")

plt.title("Monthly Sales vs Profit")
plt.xlabel("Month")
plt.ylabel("Amount (₹)")
plt.legend()

save_chart("monthly_sales_profit.png")


# 3. Sales by Category
by_category = sales_by_category(df)

plt.figure(figsize=(8,5))

plt.bar(
    by_category["product_category"],
    by_category["sales_amount"]
)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales (₹)")

plt.xticks(rotation=45)

save_chart("sales_by_category.png")


# 4. Top Products
top = top_products(df)

plt.figure(figsize=(10,5))

plt.bar(
    top["product_name"],
    top["sales_amount"]
)

plt.title("Top 10 Products by Sales")
plt.xlabel("Product")
plt.ylabel("Sales (₹)")

plt.xticks(rotation=90)

save_chart("top_products.png")

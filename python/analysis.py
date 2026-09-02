import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

import os

current_dir = os.path.dirname(__file__)

df = pd.read_csv(
    os.path.join(current_dir, "..", "data", "retail_sales_cleaned.csv")
)

df["order_date"] = pd.to_datetime(df["order_date"])

def monthly_sales(df):

    return (
        df.groupby(df["order_date"].dt.to_period("M"))["sales_amount"]
        .sum()
        .reset_index()
    )


def yearly_sales(df):

    return (
        df.groupby(df["order_date"].dt.to_period("Y"))["sales_amount"]
        .sum()
        .reset_index()
    )


def sales_by_category(df):

    return (
        df.groupby("product_category")["sales_amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def top_products(df):

    return (
        df.groupby(["product_name", "product_category"])["sales_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


def regional_sales(df):

    return (
        df.groupby("region")["sales_amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    
print("\n=== MONTHLY SALES ===")
print(monthly_sales(df))

print("\n=== YEARLY SALES ===")
print(yearly_sales(df))

print("\n=== SALES BY CATEGORY ===")
print(sales_by_category(df))

print("\n=== TOP PRODUCTS ===")
print(top_products(df))

print("\n=== REGIONAL SALES ===")
print(regional_sales(df))
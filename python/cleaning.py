import kagglehub
import pandas as pd
import os
import numpy as np

# ==============================================================================
# 1. DOWNLOAD AND LOAD DATASET
# ==============================================================================
path = kagglehub.dataset_download("satyakidas07/retail-sales-dataset")
csv_path = os.path.join(path, "retail_sales_dataset.csv")
df = pd.read_csv(csv_path)

print("=== DATA LOADED SUCCESSFULLY ===")

# ==============================================================================
# 2. STEP-BY-STEP ANALYST CLEANING PIPELINE
# ==============================================================================

# Step A: Remove completely blank rows first (like row 66)
df.dropna(how='all', inplace=True)

# Step B: Remove ghost orders missing critical identifiers
df.dropna(subset=['order_id', 'customer_id'], inplace=True)


# Step C: Turn impossible values (negatives AND 999 placeholders) into NaN
# This is crucial so they don't corrupt the median calculation!
df['age'] = df['age'].mask((df['age'] < 0) | (df['age'] > 120))
df['quantity'] = df['quantity'].mask((df['quantity'] < 0) | (df['quantity'] == 999))
df['days_to_ship'] = df['days_to_ship'].mask((df['days_to_ship'] < 0) | (df['days_to_ship'] == 100))
df['shipping_cost'] = df['shipping_cost'].mask(df['shipping_cost'] < 0)


# Step D: Handle Text/Categorical missing values
text_fills = {
    'gender': 'Unknown',
    'region': 'Unknown',
    'city': 'Unknown',
    'payment_method': 'Unknown',
    'order_status': 'Unknown',
    'customer_name': 'Unknown Customer'
}
df.fillna(text_fills, inplace=True)


# Step E: Handle Numerical missing values using the clean medians
numeric_fills = {
    'age': df['age'].median(),
    'quantity': 0,
    'discount_pct': 0,
    'shipping_cost': df['shipping_cost'].median(),
    'days_to_ship': df['days_to_ship'].median(),
    'customer_satisfaction': df['customer_satisfaction'].median(),
    'return_flag': False
}
df.fillna(numeric_fills, inplace=True)


# Step F: Fix calculated financial columns 
if 'unit_price' in df.columns:
    df['sales_amount'] = df['quantity'] * df['unit_price'] * (1 - df['discount_pct'])

df.drop_duplicates(inplace=True)

# ==============================================================================
# 3. CORRECT DATA TYPES (The final step once all NaNs are gone)
# ==============================================================================

# 1. Cast numerical metrics to clean integers
int_columns = ['age', 'quantity', 'days_to_ship', 'customer_satisfaction']
for col in int_columns:
    if col in df.columns:
        df[col] = df[col].astype(int)

# 2. Standardise and cast text/categorical entries to strings
str_columns = ['gender', 'region', 'city', 'payment_method', 'order_status', 'customer_name', 'product_category', 'product_name']
for col in str_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.title() # .title() fixes messy cases like 'FEMALE' vs 'Female'

# 3. Convert dates to proper uniform datetime format
if 'order_date' in df.columns:
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# ==============================================================================
# 4. POST-CLEANING VALIDATION CHECK
# ==============================================================================
print("\n=== POST-CLEANING VALIDATION ===")
print(f"Cleaned Min Age (Should be > 0): {df['age'].min()}")
print(f"Cleaned Max Age (Should be < 120): {df['age'].max()}")
print(f"Cleaned Max Quantity (Should be reasonable): {df['quantity'].max()}")
print("\n--- FINAL DATATYPES AND HOLES ---")
print(df.info())
print("\nRemaining Missing Values:")
print(df.isna().sum())
print(f"Final Row Count after removing duplicates: {len(df)}")

# Force pandas to check multiple date formats intelligently
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

# Drop any remaining rows that have no valid date (crucial for time series)
df.dropna(subset=['order_date'], inplace=True)

# Drop your 109 duplicates
df.drop_duplicates(inplace=True)

df.to_csv('retail_sales_cleaned.csv', index=False)

df = df.reset_index(drop=True)
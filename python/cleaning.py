import kagglehub
import pandas as pd
import os

current_dir = os.path.dirname(__file__)
output_path = os.path.join(current_dir, "..", "data", "retail_sales_cleaned.csv")

# ==============================================================================
# 1. DOWNLOAD AND LOAD DATASET
# ==============================================================================
path = kagglehub.dataset_download("satyakidas07/retail-sales-dataset")
csv_path = os.path.join(path, "retail_sales_dataset.csv")
df = pd.read_csv(csv_path)

print("=== DATA LOADED SUCCESSFULLY ===")
print(f"Raw row count: {len(df)}")

# ==============================================================================
# 2. STEP-BY-STEP ANALYST CLEANING PIPELINE
# ==============================================================================

# Step A: Remove completely blank rows first (like row 66)
df.dropna(how='all', inplace=True)

# Step B: Remove ghost orders missing critical identifiers
df.dropna(subset=['order_id', 'customer_id'], inplace=True)


# Step C: Turn impossible values (negatives AND 999 placeholders) into NaN
# This is crucial so they don't corrupt the median calculation!
df['age'] = df['age'].mask((df['age'] <= 0) | (df['age'] > 120))
df['quantity'] = df['quantity'].mask((df['quantity'] <= 0) | (df['quantity'] == 999))
df['days_to_ship'] = df['days_to_ship'].mask((df['days_to_ship'] < 0) | (df['days_to_ship'] == 100))
df['shipping_cost'] = df['shipping_cost'].mask(df['shipping_cost'] < 0)


# Step D: Drop orders with no valid quantity
# Filling these with 0 would leave orders with sales and profit but no units sold.
missing_quantity = df['quantity'].isna().sum()
df.dropna(subset=['quantity'], inplace=True)
print(f"Dropped rows with missing/invalid quantity: {missing_quantity}")


# Step E: Handle Text/Categorical missing values
text_fills = {
    'gender': 'Unknown',
    'region': 'Unknown',
    'city': 'Unknown',
    'payment_method': 'Unknown',
    'order_status': 'Unknown',
    'customer_name': 'Unknown Customer'
}
df.fillna(text_fills, inplace=True)


# Step F: Handle Numerical missing values using the clean medians
numeric_fills = {
    'age': df['age'].median(),
    'discount_pct': 0,
    'shipping_cost': df['shipping_cost'].median(),
    'days_to_ship': df['days_to_ship'].median(),
    'customer_satisfaction': df['customer_satisfaction'].median(),
    'return_flag': False
}
df.fillna(numeric_fills, inplace=True)

# Note: sales_amount is kept as provided. It does not reconcile with
# quantity * unit_price * (1 - discount_pct) in the source data, and profit is
# derived from the source sales_amount - recalculating sales alone would make
# profit exceed sales on some orders.

# ==============================================================================
# 3. CORRECT DATA TYPES (The final step once all NaNs are gone)
# ==============================================================================

# 1. Cast numerical metrics to clean integers
int_columns = ['age', 'quantity', 'days_to_ship', 'customer_satisfaction']
for col in int_columns:
    df[col] = df[col].astype(int)

df['return_flag'] = df['return_flag'].astype(bool)

# 2. Standardise and cast text/categorical entries to strings
str_columns = ['gender', 'region', 'city', 'payment_method', 'order_status', 'customer_name', 'product_category', 'product_name']
for col in str_columns:
    df[col] = df[col].astype(str).str.title() # .title() fixes messy cases like 'FEMALE' vs 'Female'

# 3. Convert dates, checking multiple date formats
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

# Drop any remaining rows that have no valid date (crucial for time series)
missing_dates = df['order_date'].isna().sum()
df.dropna(subset=['order_date'], inplace=True)
print(f"Dropped rows with missing/invalid order_date: {missing_dates}")

# 4. Remove duplicate orders
duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"Dropped duplicate rows: {duplicates}")

df = df.reset_index(drop=True)

# ==============================================================================
# 4. POST-CLEANING VALIDATION CHECK
# ==============================================================================
assert df.isna().sum().sum() == 0, "Cleaned data still has missing values"
assert df['age'].between(1, 120).all(), "Age out of range"
assert (df['quantity'] > 0).all(), "Quantity must be positive"
assert (df['profit'] <= df['sales_amount']).all(), "Profit cannot exceed sales"
assert not df['order_id'].duplicated().any(), "Duplicate order_id found"

print("\n=== POST-CLEANING VALIDATION PASSED ===")
print(f"Age range: {df['age'].min()} - {df['age'].max()}")
print(f"Max quantity: {df['quantity'].max()}")
print(f"Final row count: {len(df)} rows x {df.shape[1]} columns")

df.to_csv(output_path, index=False)
print(f"Saved cleaned dataset to {os.path.normpath(output_path)}")

import pandas as pd
import numpy as np

# Read CSV file using Pandas
df = pd.read_csv("data/fashion_sales.csv")

print("\n--- DATASET LOADED SUCCESSFULLY ---")

# Display first 10 rows
print("\nFirst 10 Records:")
print(df.head(10))

# Dataset information
print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Remove cancelled orders for sales analysis
sales_df = df[df["order_status"] != "Cancelled"].copy()

print("\n--- PANDAS ANALYSIS ---")

print("Total Valid Sales Records:", len(sales_df))

print("Total Revenue:", sales_df["total_sales"].sum())

print("Total Quantity Sold:", sales_df["quantity"].sum())

print("\nSales by Category:")

category_sales = (
    sales_df.groupby("category")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

print(category_sales)

print("\nSales by Product:")

product_sales = (
    sales_df.groupby("product_name")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

print(product_sales)


# NumPy Analysis

sales_array = sales_df["total_sales"].to_numpy()

print("\n--- NUMPY ANALYSIS ---")

print("Average Sale:", np.mean(sales_array))

print("Highest Sale:", np.max(sales_array))

print("Lowest Sale:", np.min(sales_array))

print("Standard Deviation:", np.std(sales_array))

print("Median Sale:", np.median(sales_array))
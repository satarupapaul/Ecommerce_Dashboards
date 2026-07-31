import pandas as pd
import numpy as np
from database import get_connection

connection = get_connection()

query = """
SELECT
    o.order_id,
    o.order_date,
    o.order_status,
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    p.brand,
    p.price,
    oi.quantity,
    (p.price * oi.quantity) AS total_sales
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
"""

sales_df = pd.read_sql(query, connection)

print("\n--- COMPLETE SALES DATA ---")
print(sales_df)


# PANDAS ANALYSIS

print("\n--- PANDAS SALES ANALYSIS ---")

print("Total Revenue:", sales_df["total_sales"].sum())

print("Total Quantity Sold:", sales_df["quantity"].sum())

print("\nSales by Product:")
print(
    sales_df.groupby("product_name")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Category:")
print(
    sales_df.groupby("category")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)


# NUMPY ANALYSIS

sales_array = sales_df["total_sales"].to_numpy()

print("\n--- NUMPY SALES ANALYSIS ---")

print("Average Sale:", np.mean(sales_array))

print("Highest Sale:", np.max(sales_array))

print("Lowest Sale:", np.min(sales_array))


connection.close()
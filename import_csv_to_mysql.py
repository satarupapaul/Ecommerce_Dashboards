import pandas as pd
from database import get_connection

# Read CSV file
df = pd.read_csv("data/fashion_sales.csv")

# Connect to MySQL
connection = get_connection()
cursor = connection.cursor()

# Create a new table for CSV dataset
cursor.execute("""
CREATE TABLE IF NOT EXISTS fashion_sales_data (
    order_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    city VARCHAR(50),
    quantity INT,
    price DECIMAL(10,2),
    order_status VARCHAR(50),
    total_sales DECIMAL(10,2)
)
""")

# Clear old data before importing again
cursor.execute("DELETE FROM fashion_sales_data")

# Insert CSV records into MySQL
insert_query = """
INSERT INTO fashion_sales_data
(order_id, product_name, category, brand, city,
quantity, price, order_status, total_sales)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    values = (
        int(row["order_id"]),
        row["product_name"],
        row["category"],
        row["brand"],
        row["city"],
        int(row["quantity"]),
        float(row["price"]),
        row["order_status"],
        float(row["total_sales"])
    )

    cursor.execute(insert_query, values)

# Save changes
connection.commit()

print("CSV dataset imported into MySQL successfully!")
print("Total Records Imported:", len(df))

cursor.close()
connection.close()
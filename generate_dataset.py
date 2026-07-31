import pandas as pd
import numpy as np

number_of_records = 500

# Product information
product_data = {
    "Oversized T-Shirt": ("T-Shirts", "UrbanStyle", 799),
    "Slim Fit Jeans": ("Jeans", "DenimCo", 1499),
    "Cargo Pants": ("Pants", "StreetWear", 1299),
    "Floral Summer Dress": ("Dresses", "FashionHub", 1799),
    "Denim Jacket": ("Jackets", "DenimCo", 2499),
    "Crop Top": ("Tops", "UrbanStyle", 699),
    "Formal Shirt": ("Shirts", "ClassicWear", 1199),
    "Hoodie": ("Winter Wear", "StreetWear", 1599),
    "Pleated Skirt": ("Skirts", "FashionHub", 999),
    "Casual Kurti": ("Ethnic Wear", "EthnicStyle", 1399),
    "Wide Leg Jeans": ("Jeans", "DenimCo", 1699),
    "Graphic T-Shirt": ("T-Shirts", "UrbanStyle", 899),
    "Bodycon Dress": ("Dresses", "FashionHub", 1999),
    "Bomber Jacket": ("Jackets", "StreetWear", 2799),
    "Palazzo Pants": ("Pants", "EthnicStyle", 1099)
}

cities = [
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Kolkata",
    "Chennai",
    "Hyderabad",
    "Pune",
    "Ahmedabad"
]

order_statuses = [
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled"
]

np.random.seed(42)

product_names = list(product_data.keys())

selected_products = np.random.choice(
    product_names,
    number_of_records
)

data = []

for order_id, product in enumerate(selected_products, start=1):

    category = product_data[product][0]
    brand = product_data[product][1]
    price = product_data[product][2]

    quantity = np.random.randint(1, 6)

    city = np.random.choice(cities)

    order_status = np.random.choice(order_statuses)

    data.append([
        order_id,
        product,
        category,
        brand,
        city,
        quantity,
        price,
        order_status
    ])

df = pd.DataFrame(
    data,
    columns=[
        "order_id",
        "product_name",
        "category",
        "brand",
        "city",
        "quantity",
        "price",
        "order_status"
    ]
)

# Calculate total sales
df["total_sales"] = df["price"] * df["quantity"]

# Save dataset
df.to_csv(
    "data/fashion_sales.csv",
    index=False
)

print("Fashion sales CSV dataset created successfully!")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 10 Records:")
print(df.head(10))
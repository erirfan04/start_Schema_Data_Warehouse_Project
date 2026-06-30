import pandas as pd

# =====================================================
# STEP 1 : Read CSV File
# =====================================================

print("="*60)
print("STEP 1 : READ CSV FILE")
print("="*60)

df = pd.read_csv("sales.csv")

print(df)

# =====================================================
# STEP 2 : Create Customer Dimension
# =====================================================

print("\n")
print("="*60)
print("STEP 2 : CUSTOMER DIMENSION")
print("="*60)

customer_dim = (
    df[["CustomerName", "City"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

customer_dim["CustomerID"] = customer_dim.index + 1

customer_dim = customer_dim[
    ["CustomerID", "CustomerName", "City"]
]

print(customer_dim)

# =====================================================
# STEP 3 : Create Product Dimension
# =====================================================

print("\n")
print("="*60)
print("STEP 3 : PRODUCT DIMENSION")
print("="*60)

product_dim = (
    df[["ProductName", "Category", "Price"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

product_dim["ProductID"] = product_dim.index + 1

product_dim = product_dim[
    ["ProductID", "ProductName", "Category", "Price"]
]

print(product_dim)

# =====================================================
# STEP 4 : Create Date Dimension
# =====================================================

print("\n")
print("="*60)
print("STEP 4 : DATE DIMENSION")
print("="*60)

date_dim = (
    df[["OrderDate"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

date_dim["OrderDate"] = pd.to_datetime(date_dim["OrderDate"])

date_dim["DateID"] = date_dim.index + 1

date_dim["Year"] = date_dim["OrderDate"].dt.year
date_dim["Month"] = date_dim["OrderDate"].dt.month
date_dim["Day"] = date_dim["OrderDate"].dt.day

date_dim = date_dim[
    ["DateID", "OrderDate", "Year", "Month", "Day"]
]

print(date_dim)

# =====================================================
# STEP 5 : Build Fact Table
# =====================================================

print("\n")
print("="*60)
print("STEP 5 : FACT TABLE")
print("="*60)

fact = df.merge(
    customer_dim,
    on=["CustomerName", "City"]
)

fact = fact.merge(
    product_dim,
    on=["ProductName", "Category", "Price"]
)

fact["OrderDate"] = pd.to_datetime(fact["OrderDate"])

fact = fact.merge(
    date_dim,
    on="OrderDate"
)

fact_sales = fact[
    [
        "OrderID",
        "DateID",
        "CustomerID",
        "ProductID",
        "Quantity",
        "Price"
    ]
]

print(fact_sales)

# =====================================================
# STEP 6 : Save CSV Files
# =====================================================

customer_dim.to_csv(
    "dim_customer.csv",
    index=False
)

product_dim.to_csv(
    "dim_product.csv",
    index=False
)

date_dim.to_csv(
    "dim_date.csv",
    index=False
)

fact_sales.to_csv(
    "fact_sales.csv",
    index=False
)

print("\n")
print("="*60)
print("CSV FILES CREATED SUCCESSFULLY")
print("="*60)

print("dim_customer.csv")
print("dim_product.csv")
print("dim_date.csv")
print("fact_sales.csv")
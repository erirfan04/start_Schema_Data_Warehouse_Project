import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# Connect MySQL
# ============================================================

engine = create_engine(
    "mysql+pymysql://root:root@localhost/datawarehouse"
)

# ============================================================
# Read CSV
# ============================================================

df = pd.read_csv("sales.csv")

print("="*60)
print("ORIGINAL DATA")
print("="*60)
print(df)

# ============================================================
# CUSTOMER DIMENSION
# ============================================================

customer_dim = (
    df[["CustomerName","City"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

customer_dim["CustomerID"] = customer_dim.index + 1

customer_dim = customer_dim[
    ["CustomerID","CustomerName","City"]
]

print("\nCustomer Dimension")
print(customer_dim)

# ============================================================
# PRODUCT DIMENSION
# ============================================================

product_dim = (
    df[["ProductName","Category","Price"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

product_dim["ProductID"] = product_dim.index + 1

product_dim = product_dim[
    ["ProductID","ProductName","Category","Price"]
]

print("\nProduct Dimension")
print(product_dim)

# ============================================================
# DATE DIMENSION
# ============================================================

date_dim = (
    df[["OrderDate"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

date_dim["OrderDate"] = pd.to_datetime(
    date_dim["OrderDate"]
)

date_dim["DateID"] = date_dim.index + 1

date_dim["Year"] = date_dim["OrderDate"].dt.year
date_dim["Month"] = date_dim["OrderDate"].dt.month
date_dim["Day"] = date_dim["OrderDate"].dt.day

date_dim = date_dim[
    ["DateID","OrderDate","Year","Month","Day"]
]

print("\nDate Dimension")
print(date_dim)

# ============================================================
# FACT TABLE
# ============================================================

fact = df.merge(
    customer_dim,
    on=["CustomerName","City"]
)

fact = fact.merge(
    product_dim,
    on=["ProductName","Category","Price"]
)

fact["OrderDate"] = pd.to_datetime(
    fact["OrderDate"]
)

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

print("\nFact Table")
print(fact_sales)

# ============================================================
# LOAD INTO MYSQL
# ============================================================

# append because tables already exist

customer_dim.to_sql(
    "dim_customer",
    con=engine,
    if_exists="append",
    index=False
)

product_dim.to_sql(
    "dim_product",
    con=engine,
    if_exists="append",
    index=False
)

date_dim.to_sql(
    "dim_date",
    con=engine,
    if_exists="append",
    index=False
)

fact_sales.to_sql(
    "fact_sales",
    con=engine,
    if_exists="append",
    index=False
)

print("\n")
print("="*60)
print("DATA LOADED SUCCESSFULLY")
print("="*60)
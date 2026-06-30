
#pip install sqlalchemy
#python -m pip install pymysql
#python -m pip install pandas

Project Flow
                  sales.csv
                      │
                      ▼
                Read using Python
                      │
                      ▼
            Create Dimension Tables
                      │
                      ▼
             Create Fact Table
                      │
                      ▼
          Insert into Existing MySQL Tables
Step 1: Create Database
CREATE DATABASE datawarehouse;

USE datawarehouse;
Step 2: Create Tables in MySQL
Customer Dimension
CREATE TABLE dim_customer
(
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    City VARCHAR(100)
);
Product Dimension
CREATE TABLE dim_product
(
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(100),
    Price DECIMAL(10,2)
);
Date Dimension
CREATE TABLE dim_date
(
    DateID INT PRIMARY KEY,
    OrderDate DATE,
    Year INT,
    Month INT,
    Day INT
);
Fact Table
CREATE TABLE fact_sales
(
    OrderID INT PRIMARY KEY,

    DateID INT,

    CustomerID INT,

    ProductID INT,

    Quantity INT,

    Price DECIMAL(10,2),

    CONSTRAINT FK_DATE
        FOREIGN KEY(DateID)
        REFERENCES dim_date(DateID),

    CONSTRAINT FK_CUSTOMER
        FOREIGN KEY(CustomerID)
        REFERENCES dim_customer(CustomerID),

    CONSTRAINT FK_PRODUCT
        FOREIGN KEY(ProductID)
        REFERENCES dim_product(ProductID)
);

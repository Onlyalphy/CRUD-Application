# FastAPI E-commerce CRUD (Assignment deliverable)

## Prerequisites
- Python 3.8+
- MySQL server (local or remote)
- pip

## Setup DB
1. Create database & tables:
   mysql -u root -p < ecommerce_schema.sql

   (or run the SQL in your MySQL client)

2. Optionally, verify that `ecommerce_db` exists and that `customers`, `products`, `orders`, `order_items` tables were created.

## Python app setup
1. Create virtualenv and install:
   python -m venv venv
   source venv/bin/activate   # windows: venv\Scripts\activate
   pip install -r requirements.txt

   If you get trouble installing `mysqlclient`, install `PyMySQL` and adjust `requirements.txt` accordingly.

2. Configure DB connection
   Create a `.env` file in project root with:

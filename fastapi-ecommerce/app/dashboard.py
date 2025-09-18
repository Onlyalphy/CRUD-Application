# dashboard.py
import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load DB connection
load_dotenv()
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("📊 E-commerce Dashboard")

# Helper to load tables
def load_table(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

# Insert helpers
def insert_customer(full_name, email, phone):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO customers (full_name, email, phone) VALUES (:n,:e,:p)"),
            {"n": full_name, "e": email, "p": phone},
        )

def insert_product(name, description, price, sku, stock_qty):
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO products (name, description, price, sku, stock_qty) "
                "VALUES (:n,:d,:pr,:s,:q)"
            ),
            {"n": name, "d": description, "pr": price, "s": sku, "q": stock_qty},
        )

def insert_order(customer_id, items):
    """items = list of dicts: [{'product_id':..,'qty':..,'price':..}]"""
    with engine.begin() as conn:
        # Create order
        res = conn.execute(
            text("INSERT INTO orders (customer_id, total_amount) VALUES (:c,0)"),
            {"c": customer_id},
        )
        order_id = res.lastrowid
        total = 0
        for it in items:
            line_total = float(it["price"]) * int(it["qty"])
            total += line_total
            conn.execute(
                text(
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) "
                    "VALUES (:o,:p,:q,:pr)"
                ),
                {"o": order_id, "p": it["product_id"], "q": it["qty"], "pr": it["price"]},
            )
            # Decrement stock
            conn.execute(
                text("UPDATE products SET stock_qty = stock_qty - :q WHERE product_id=:p"),
                {"q": it["qty"], "p": it["product_id"]},
            )
        # Update total
        conn.execute(
            text("UPDATE orders SET total_amount=:t WHERE order_id=:o"),
            {"t": total, "o": order_id},
        )
    return order_id

# Sidebar menu
menu = st.sidebar.radio("Navigate", ["Customers", "Products", "Orders", "Order Items", "Analytics", "➕ Add Records"])

# Data views
if menu == "Customers":
    st.header("👤 Customers")
    st.dataframe(load_table("customers"))

elif menu == "Products":
    st.header("📦 Products")
    st.dataframe(load_table("products"))

elif menu == "Orders":
    st.header("🛒 Orders")
    st.dataframe(load_table("orders"))

elif menu == "Order Items":
    st.header("📋 Order Items")
    st.dataframe(load_table("order_items"))

elif menu == "Analytics":
    st.header("📈 Analytics")

    orders = load_table("orders")
    order_items = load_table("order_items")
    products = load_table("products")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Orders by Status")
        if not orders.empty:
            st.bar_chart(orders["status"].value_counts())
        else:
            st.info("No orders yet.")

    with col2:
        st.subheader("Top Products by Quantity")
        if not order_items.empty:
            merged = order_items.merge(products, on="product_id")
            top_products = merged.groupby("name")["quantity"].sum().sort_values(ascending=False)
            st.bar_chart(top_products)
        else:
            st.info("No order items yet.")

elif menu == "➕ Add Records":
    st.header("➕ Insert New Records")

    tab1, tab2, tab3 = st.tabs(["Customer", "Product", "Order"])

    with tab1:
        st.subheader("Add Customer")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        if st.button("Add Customer"):
            if name and email:
                insert_customer(name, email, phone)
                st.success("✅ Customer added!")
            else:
                st.error("Name and Email are required.")

    with tab2:
        st.subheader("Add Product")
        pname = st.text_input("Product Name")
        desc = st.text_area("Description")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        sku = st.text_input("SKU")
        qty = st.number_input("Stock Quantity", min_value=0, step=1)
        if st.button("Add Product"):
            if pname and sku:
                insert_product(pname, desc, price, sku, qty)
                st.success("✅ Product added!")
            else:
                st.error("Name and SKU are required.")

    with tab3:
        st.subheader("Create Order")
        customers = load_table("customers")
        products = load_table("products")

        if customers.empty or products.empty:
            st.info("Need at least one customer and one product.")
        else:
            cust_map = dict(zip(customers["full_name"], customers["customer_id"]))
            chosen_customer = st.selectbox("Select Customer", list(cust_map.keys()))

            selected_items = []
            with st.form("order_form", clear_on_submit=True):
                st.write("Add Products to Order")
                prod_map = dict(zip(products["name"], products["product_id"]))
                prod_name = st.selectbox("Product", list(prod_map.keys()))
                qty = st.number_input("Quantity", min_value=1, step=1)
                price = st.number_input("Unit Price", min_value=0.01, step=0.01)
                submitted = st.form_submit_button("Add Product to Order")
                if submitted:
                    selected_items.append(
                        {"product_id": prod_map[prod_name], "qty": qty, "price": price}
                    )
                    st.success(f"Added {qty} x {prod_name}")

            if st.button("Place Order"):
                if selected_items:
                    order_id = insert_order(cust_map[chosen_customer], selected_items)
                    st.success(f"✅ Order {order_id} created!")
                else:
                    st.error("Add at least one product to order.")

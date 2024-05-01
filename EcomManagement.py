import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
conn = sqlite3.connect('ecommerce_new.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS Customer (
                    CustomerID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Email TEXT NOT NULL,
                    Gender TEXT NOT NULL,
                    Phone TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Product (
                    ProductID INTEGER PRIMARY KEY,
                    ProductName TEXT,
                    Price REAL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS OrderTable (
                    OrderID INTEGER PRIMARY KEY,
                    Customer TEXT,
                    Product TEXT,
                    Quantity INTEGER,
                    Total INTERGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Payment (
                    PaymentID INTEGER PRIMARY KEY,
                    PaymentDate TEXT,
                    Amount REAL,
                    OrderID INTEGER,
                    FOREIGN KEY (OrderID) REFERENCES OrderTable(OrderID))''')

    c.execute('''CREATE TABLE IF NOT EXISTS Delivery (
                    DeliveryID INTEGER PRIMARY KEY,
                    DeliveryDate TEXT,
                    Status TEXT,
                    OrderID INTEGER,
                    FOREIGN KEY (OrderID) REFERENCES OrderTable(OrderID))''')

    c.execute('''CREATE TABLE IF NOT EXISTS Address (
                    CusID INTEGER PRIMARY KEY,
                    house TEXT,
                    city TEXT,
                    state TEXT,
                    zip TEXT,
                    FOREIGN KEY (CusID) REFERENCES Customer(CustomerID))''')
    conn.commit()

def add_customer():
    st.subheader("Add New Customer")
    cusID = st.number_input("Customer ID",value=0)
    name = st.text_input("Name")
    mail = st.text_input("E-Mail")
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    phone =  st.text_input("Phone")
    if st.button("Add Customer"):
        c.execute("INSERT INTO Customer (CustomerID, Name, Email, Gender, Phone) VALUES (?,?,?,?,?)", (cusID, name, mail, gender, phone))
        conn.commit()
        st.success("Customer added successfully!")

def view_customers():
    st.subheader("Customer Records")
    customers = c.execute("SELECT * FROM Customer").fetchall()
    df_customers = pd.DataFrame(customers, columns=["CustomerID", "Name", "Email", "Gender", "Phone"])
    df_customer = df_customers.reset_index(drop=True)
    st.dataframe(df_customer)

def add_address():
    st.subheader("Add Address")
    customers = c.execute("SELECT * FROM Customer").fetchall()
    customer_names = [customer[0] for customer in customers]
    selected_customer = st.selectbox("Select Customer ID", customer_names)
    selected_customer_name = c.execute("SELECT Name FROM Customer WHERE CustomerID=?", (selected_customer,)).fetchone()[0]
    st.write("Selected Customer Name: ", selected_customer_name)
    house = st.text_input("House/Office Number")
    city = st.text_input("City")
    state = st.text_input("State")
    zip_code = st.text_input("Zip Code")
    
    if st.button("Add Address"):
        cus_id = next(item[0] for item in customers if item[0] == selected_customer)
        c.execute("INSERT INTO Address (CusID, house, city, state, zip) VALUES (?,?,?,?,?)",
                  (cus_id, house, city, state, zip_code))
        conn.commit()
        st.success("Address Added Successfully")

def view_address():
    st.subheader("Address Records")
    address = c.execute("SELECT * FROM Address").fetchall()
    df_address = pd.DataFrame(address, columns=["CustomerID", "House", "City", "State", "Zip Code"])
    df_address = df_address.reset_index(drop=True)
    st.dataframe(df_address)
    
def add_product(name, price):
    c.execute('''INSERT INTO Product (ProductName, Price) VALUES (?, ?)''', (name, price))
    conn.commit()
    st.success("Product added successfully!")

def view_products():
    st.write("### Products:")
    products = c.execute("SELECT * FROM Product").fetchall()
    df_products = pd.DataFrame(products, columns=["ProductID", "Product Name", "Price"])
    df_products = df_products.reset_index(drop=True)
    st.dataframe(df_products)

def view_orders():
    st.write("### Orders:")
    orders = c.execute("SELECT * FROM OrderTable").fetchall()
    orders_ = pd.DataFrame(orders, columns=["OrderID", "Customer", "Product", "Quantity", "Total"])
    orders_ = orders_.reset_index(drop=True)
    st.dataframe(orders_)

def manage_products():
    st.subheader("Product Management")
    name = st.text_input("Product Name")
    price = st.number_input("Price", value=0)
    if st.button("Add Product"):
        add_product(name, price)
    view_products()

def place_an_order():
    st.subheader("Place an Order")

    customers = c.execute("SELECT * FROM Customer").fetchall()
    customer_names = [customer[0] for customer in customers]
    selected_customer = st.selectbox("Select Customer ID", customer_names)
    selected_customer_name = c.execute("SELECT Name FROM Customer WHERE CustomerID=?", (selected_customer,)).fetchone()[0]
    st.write("Selected Customer Name: ", selected_customer_name)

    products = c.execute("SELECT * FROM Product").fetchall()
    product_names = [product[0] for product in products]
    selected_product= st.selectbox("Select Product ID", product_names)
    selected_product_name = c.execute("SELECT ProductName FROM Product WHERE ProductID=?", (selected_product,)).fetchone()[0]
    st.write("Selected Customer Name: ", selected_product_name)

    quantity = st.number_input("Quantity", value=1)
    orderID = st.number_input("Order ID",value=0)
    if st.button("Place Order"):
        total_amount = c.execute('''SELECT Price * ? FROM Product WHERE ProductID = ?''', (quantity, selected_product)).fetchone()[0]
        c.execute('''INSERT INTO OrderTable (OrderID, Customer, Product, Quantity, Total) VALUES (?, ?, ?, ?, ?)''', (orderID, selected_customer_name, selected_product_name, quantity, total_amount))
        conn.commit()
        st.success("Order placed successfully!")
def delete_customer():
    st.subheader("Delete Customer")
    customers = c.execute("SELECT * FROM Customer").fetchall()
    customer_ids = [customer[0] for customer in customers]
    selected_customer_id = st.selectbox("Select Customer ID to Delete", customer_ids)
    selected_customer_name = c.execute("SELECT Name FROM Customer WHERE CustomerID=?", (selected_customer_id,)).fetchone()[0]
    st.write("Selected Customer Name: ", selected_customer_name)

    if st.button("Delete Customer"):
        c.execute("DELETE FROM Customer WHERE CustomerID=?", (selected_customer_id,))
        conn.commit()
        st.success(f"Customer '{selected_customer_name}' deleted successfully!")

def delete_product():
    st.subheader("Delete Product")
    products = c.execute("SELECT * FROM Product").fetchall()
    product_ids = [product[0] for product in products]
    selected_product_id = st.selectbox("Select Product ID to Delete", product_ids)
    selected_product_name = c.execute("SELECT ProductName FROM Product WHERE ProductID=?", (selected_product_id,)).fetchone()[0]
    st.write("Selected Product Name: ", selected_product_name)

    if st.button("Delete Product"):
        c.execute("DELETE FROM Product WHERE ProductID=?", (selected_product_id,))
        conn.commit()
        st.success(f"Product '{selected_product_name}' deleted successfully!")

def delete_order():
    st.subheader("Delete Order")
    orders = c.execute("SELECT * FROM OrderTable").fetchall()
    order_ids = [order[0] for order in orders]
    selected_order_id = st.selectbox("Select Order ID to Delete", order_ids)
    selected_order_info = c.execute("SELECT Customer, Product FROM OrderTable WHERE OrderID=?", (selected_order_id,)).fetchone()
    st.write("Selected Order Customer: ", selected_order_info[0])
    st.write("Selected Order Product: ", selected_order_info[1])

    if st.button("Delete Order"):
        c.execute("DELETE FROM OrderTable WHERE OrderID=?", (selected_order_id,))
        conn.commit()
        st.success("Order deleted successfully!")

def delete_address():
    st.subheader("Delete Address")
    addresses = c.execute("SELECT * FROM Address").fetchall()
    address_ids = [address[0] for address in addresses]
    selected_address_id = st.selectbox("Select Address ID to Delete", address_ids)
    selected_address_info = c.execute("SELECT house, city, state, zip FROM Address WHERE CusID=?", (selected_address_id,)).fetchone()
    st.write("Selected Address: ", ", ".join(selected_address_info))

    if st.button("Delete Address"):
        c.execute("DELETE FROM Address WHERE CusID=?", (selected_address_id,))
        conn.commit()
        st.success("Address deleted successfully!")
def main():
    st.title("E-commerce Management System")
    navigation_options = st.sidebar.selectbox("Navigation",     ["Home","Register", "Add Address", "Manage Products", "Place Order", "View Customers", "View Address", "View Orders", "Delete Customer", "Delete Product", "Delete Order", "Delete Address"], index=0)

    if navigation_options == "Home":
        st.subheader("Home")
        st.markdown("<h4 style='text-align: Left;'>Welcome to the E-Commerce Management System!</h4>", unsafe_allow_html=True)

    elif navigation_options == "Register":
        add_customer()
    elif navigation_options == "Add Address":
        add_address()
    elif navigation_options == "Manage Products":
        manage_products()
    elif navigation_options == "Place Order":
        place_an_order()
    elif navigation_options == "View Address":
        view_address()
    elif navigation_options == "View Customers":
        view_customers()
    elif navigation_options == "View Orders":
        view_orders()
    elif navigation_options == "Delete Customer":
        delete_customer()
    elif navigation_options == "Delete Product":
        delete_product()
    elif navigation_options == "Delete Order":
        delete_order()
    elif navigation_options == "Delete Address":
        delete_address()
if __name__ == "__main__":
    create_tables()
    main()
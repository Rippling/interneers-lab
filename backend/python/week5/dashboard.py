import streamlit as st
import pandas as pd
from week4.db_connection import initialize_mongo
from week4.models import Product, ProductCategory
from decimal import Decimal


initialize_mongo()


# page settings
st.set_page_config(page_title="Week 5 Inventory Dashboard", layout="wide")
st.title("Week 5: Interactive Data Tools")
st.write("Streamlit dashboard connected directly to MongoDB using MongoEngine")


# helpers
def get_all_categories():
    return list(ProductCategory.objects().order_by("title"))


def fetch_products(selected_category_id=None):
    if selected_category_id is None:
        products = Product.objects()
    else:
        products = Product.objects(category=selected_category_id)

    rows = []

    for product in products:
        rows.append({
            "ID": product.id,
            "Name": product.name,
            "Description": product.description,
            "Price": float(product.price),
            "Brand": product.brand,
            "Quantity": product.quantity,
            "Category": product.category.title if product.category else "No Category"
        })

    return pd.DataFrame(rows)


# creating sidebar category filter
st.sidebar.header("Filter Inventory")

all_category = get_all_categories()
# creating dictionary where all maps to none so that no conflict arises
category_options = {"All": None}

for category in all_category:
    category_options[category.title] = category.id

selected_category_title = st.sidebar.selectbox(
    "Select Product Category", list(category_options.keys()))

selected_category_id = category_options[selected_category_title]


# showing inventory table for current id
@st.fragment
def inventory_table(category_id):
    st.subheader("Current Inventory")
    df = fetch_products(category_id)
    if df.empty:
        st.info("No products found in this category")
    else:
        st.dataframe(df, use_container_width=True)
    return df


# showing stock alert
@st.fragment
def stock_alert(df):
    st.subheader("Stock Alert")
    if not df.empty:
        low_stock_row = []
        for index, row in df.iterrows():
            if row["Quantity"] < 5:
                low_stock_row.append(row)
        low_stock_df = pd.DataFrame(low_stock_row)

        if not low_stock_df.empty:
            st.error("Some products are running low in stock")
            st.dataframe(low_stock_df, use_container_width=True)
        else:
            st.success("No products are running low in stock")
    else:
        st.info("No products found in this category")


# adding product
@st.fragment
def add_product(categories):
    st.subheader("Add Product")
    category_title = []
    for category in categories:
        category_title.append(category.title)

    with st.form("add_product_form"):
        new_name = st.text_input("Name")
        new_description = st.text_area("Description")
        new_price = st.number_input(
            "Price", min_value=0.0, step=1.0, format="%.2f")
        new_brand = st.text_input("Brand")
        new_quantity = st.number_input(
            "Quantity", min_value=0, step=1)
        new_category_title = st.selectbox("Category", category_title if category_title else [
            "No categories found "])
        submitted = st.form_submit_button("Add Product")

    if submitted:
        if not new_name.strip():
            st.error("Product name cannot be empty")
        elif not new_description.strip():
            st.error("Description cannot be empty")
        elif not new_brand.strip():
            st.error("Brand cannot be empty")
        elif not new_category_title:
            st.error("No category exist. Pls create a category first in week 4")
        else:
            selected_category = ProductCategory.objects(
                title=new_category_title).first()
            Product(name=new_name, description=new_description,
                    price=Decimal(str(new_price)), brand=new_brand, quantity=int(new_quantity), category=selected_category).save()
            st.success(f"Product '{new_name}' added successfully")
            st.rerun()


# removing product
@st.fragment
def remove_product():
    st.subheader("Remove Product")
    all_products = Product.objects().order_by("name")
    product_options = {}
    for product in all_products:
        label = f"{product.name} (ID: {product.id})"
        product_options[label] = product.id

    if product_options:
        selected_product_label = st.selectbox(
            "Select Product to remove", list(product_options.keys()))
        if st.button("Remove Product"):
            selected_product_id = product_options[selected_product_label]
            Product.objects(id=selected_product_id).delete()
            st.success("Product removed successfully")
            st.rerun()
    else:
        st.info("No products found")


df = inventory_table(selected_category_id)
stock_alert(df)
add_product(all_category)
remove_product()

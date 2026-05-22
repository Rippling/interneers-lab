# pages/1_Products.py

import streamlit as st
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db_connection import connect_to_mongodb
connect_to_mongodb()

from products.models import Product
from products.category_model import ProductCategory

st.set_page_config(page_title="Products", page_icon="📦", layout="wide")

def get_all_products():
    products = Product.objects.all()
    data = []
    for p in products:
        try:
            category_title = p.category.title if p.category else "Unknown"
        except Exception:
            category_title = "Unknown"
        data.append({
            "ID": str(p.id),
            "Name": p.name,
            "Category": category_title,
            "Brand": p.brand,
            "Price (₹)": float(str(p.price)),
            "Stock": p.quantity_in_warehouse,
            "Description": p.description,
        })
    import pandas as pd
    return pd.DataFrame(data)

def get_all_categories():
    return list(ProductCategory.objects.all())

st.title("📦 Products Management")
st.markdown("---")

categories = get_all_categories()
df = get_all_products()

# ─── ADD NEW CATEGORY ──────────────────────────────────────────
st.subheader("🗂️ Add New Category")

with st.form("add_category_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_category_title = st.text_input("Category Name *")
    with col2:
        new_category_description = st.text_area("Description")

    category_submitted = st.form_submit_button("Add Category")

    if category_submitted:
        if not new_category_title:
            st.error("Category name is required!")
        else:
            try:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                existing = ProductCategory.objects(title=new_category_title).first()
                if existing:
                    st.error(f"❌ Category '{new_category_title}' already exists!")
                else:
                    category = ProductCategory(
                        title=new_category_title,
                        description=new_category_description,
                        created_at=now,
                        updated_at=now
                    )
                    category.save()
                    st.success(f"✅ Category '{new_category_title}' added successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error adding category: {e}")

st.markdown("---")

# ─── ADD PRODUCT FORM ──────────────────────────────────────────
st.subheader("➕ Add New Product")

with st.form("add_product_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Product Name *")
        new_brand = st.text_input("Brand *")
        new_price = st.number_input("Price *", min_value=0.01, value=100.0)
        new_quantity = st.number_input("Quantity", min_value=0, value=0)
    with col2:
        new_description = st.text_area("Description")
        category_titles = [c.title for c in categories]
        new_category = st.selectbox("Category *", category_titles)

    submitted = st.form_submit_button("Add Product")

    if submitted:
        if not new_name or not new_brand:
            st.error("Name and Brand are required!")
        else:
            try:
                category_obj = ProductCategory.objects.get(title=new_category)
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                product = Product(
                    name=new_name,
                    brand=new_brand,
                    price=new_price,
                    quantity_in_warehouse=new_quantity,
                    description=new_description,
                    category=category_obj,
                    created_at=now,
                    updated_at=now
                )
                product.save()
                st.success(f"✅ Product '{new_name}' added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding product: {e}")

st.markdown("---")

# ─── REMOVE PRODUCT ────────────────────────────────────────────
st.subheader("🗑️ Remove Product")

if df.empty:
    st.info("No products to remove.")
else:
    product_options = df["Name"] + " (" + df["ID"] + ")"
    selected_product = st.selectbox("Select product to remove", product_options)

    if st.button("🗑️ Delete Selected Product", type="primary"):
        product_id = selected_product.split("(")[-1].replace(")", "").strip()
        try:
            product = Product.objects.get(id=product_id)
            product_name = product.name
            product.delete()
            st.success(f"✅ Product '{product_name}' deleted successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error deleting product: {e}")
# dashboard.py — Home Page
# Run with: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db_connection import connect_to_mongodb
connect_to_mongodb()

from products.models import Product
from products.category_model import ProductCategory

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #000000 !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: #000000 !important;
        border-right: 1px solid #1e3a5f;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #112240 0%, #1a3a5c 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1rem;
    }

    /* Dataframe styling */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #1e3a5f;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1565c0, #1976d2);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2, #1565c0);
        border: none;
    }

    /* Subheader color */
    h2, h3 {
        color: #90caf9 !important;
    }

    /* Text inputs */
    .stTextInput > div > div > input {
        background: #112240;
        border: 1px solid #1e3a5f;
        color: white;
        border-radius: 8px;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #112240;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #112240;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─── HELPER FUNCTIONS ──────────────────────────────────────────
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
    return pd.DataFrame(data)

def get_all_categories():
    return list(ProductCategory.objects.all())

def color_stock(val):
    if val == 0:
        return "background-color: #7f1d1d; color: #fca5a5; font-weight: 600;"
    elif val < 10:
        return "background-color: #78350f; color: #fcd34d; font-weight: 600;"
    else:
        return "background-color: #14532d; color: #86efac; font-weight: 600;"

def style_table(df):
    styled = df.style.map(
        color_stock,
        subset=["Stock"]
    ).set_properties(**{
        "background-color": "#112240",
        "color": "#e2e8f0",
        "border-color": "#1e3a5f",
        "font-size": "13px"
    }).set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#0d1f3c"),
                ("color", "#90caf9"),
                ("font-weight", "500"),
                ("font-size", "12px"),
                ("border-bottom", "1px solid #1e3a5f"),
                ("padding", "10px 12px"),
            ]
        },
        {
            "selector": "td",
            "props": [
                ("padding", "10px 12px"),
                ("border-bottom", "1px solid #1a3a5c"),
            ]
        },
        {
            "selector": "tr:hover td",
            "props": [
                ("background-color", "#1a3a5c"),
            ]
        }
    ])
    return styled

# ─── SIDEBAR ───────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center; padding: 1rem 0 0.5rem;">
    <div style="font-size:28px; margin-bottom:4px;">📦</div>
    <p style="color:#90caf9; font-weight:500; font-size:14px; margin:0;">Inventory System</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()

st.sidebar.markdown("### 🔍 Filter Products")
categories = get_all_categories()
category_options = ["All"] + [c.title for c in categories]
selected_category = st.sidebar.selectbox("Category", category_options)
brand_filter = st.sidebar.text_input("Brand contains")
st.sidebar.markdown("### 💰 Price Range")
min_price = st.sidebar.number_input("Min Price", min_value=0, value=0)
max_price = st.sidebar.number_input("Max Price", min_value=0, value=1000000)

# ─── HEADER ────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-bottom:1.5rem;">
    <div style="
        width:44px; height:44px;
        background:linear-gradient(135deg, #1565c0, #1976d2);
        border-radius:10px;
        display:flex; align-items:center; justify-content:center;
        font-size:22px;
    ">📦</div>
    <div>
        <h1 style="margin:0; font-size:22px; font-weight:600; color:#e2e8f0;">
            Product Inventory Dashboard
        </h1>
        <p style="margin:0; font-size:13px; color:#64748b;">
            Real-time inventory overview & management
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ─────────────────────────────────────────────────
df = get_all_products()
df_all = df.copy()

if not df.empty:
    if selected_category != "All":
        df = df[df["Category"] == selected_category]
    if brand_filter:
        df = df[df["Brand"].str.contains(brand_filter, case=False)]
    df = df[(df["Price (₹)"] >= min_price) & (df["Price (₹)"] <= max_price)]

# ─── ALERT BANNERS ─────────────────────────────────────────────
if not df_all.empty:
    critical_low = df_all[df_all["Stock"] == 0]
    low_stock_items = df_all[(df_all["Stock"] > 0) & (df_all["Stock"] < 10)]

    if not critical_low.empty:
        st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #7f1d1d22, #7f1d1d44);
    border: 1px solid #ef444466;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
">
    <span style="font-size:18px;">🚨</span>
    <span style="color:#fca5a5; font-weight:500; font-size:14px;">
        {len(critical_low)} product(s) are OUT OF STOCK — immediate restocking required
    </span>
</div>
""", unsafe_allow_html=True)
        with st.expander("View Out of Stock Products"):
            st.dataframe(
                critical_low[["Name", "Category", "Brand", "Stock"]],
                hide_index=True,
                use_container_width=True
            )

    if not low_stock_items.empty:
        st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #78350f22, #78350f44);
    border: 1px solid #f59e0b66;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
">
    <span style="font-size:18px;">⚠️</span>
    <span style="color:#fcd34d; font-weight:500; font-size:14px;">
        {len(low_stock_items)} product(s) are running LOW on stock (less than 10 units)
    </span>
</div>
""", unsafe_allow_html=True)
        with st.expander("View Low Stock Products"):
            st.dataframe(
                low_stock_items[["Name", "Category", "Brand", "Stock"]],
                hide_index=True,
                use_container_width=True
            )

# ─── METRICS ───────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Total Products", len(df))
with col2:
    total_stock = int(df["Stock"].sum()) if not df.empty else 0
    st.metric("🏭 Total Stock", f"{total_stock:,}")
with col3:
    avg_price = round(df["Price (₹)"].mean(), 2) if not df.empty else 0
    st.metric("💰 Avg Price", f"₹{avg_price:,}")
with col4:
    low_stock = len(df[df["Stock"] < 10]) if not df.empty else 0
    st.metric("⚠️ Low Stock Items", low_stock)

st.markdown("<br>", unsafe_allow_html=True)

# ─── HEALTH SCORE ──────────────────────────────────────────────
st.markdown("""
<p style="font-size:16px; font-weight:500; color:#90caf9; margin-bottom:1rem;">
    📊 Inventory Health Score
</p>
""", unsafe_allow_html=True)

if not df_all.empty:
    total = len(df_all)
    in_stock = len(df_all[df_all["Stock"] > 0])
    out_of_stock = len(df_all[df_all["Stock"] == 0])
    low_stock_count = len(df_all[df_all["Stock"] < 10])
    avg_stock = df_all["Stock"].mean()
    num_categories = df_all["Category"].nunique()

    stock_score = (in_stock / total) * 40
    avg_score = min(avg_stock / 100, 1) * 30
    low_penalty = max(0, 20 - (low_stock_count * 2))
    cat_score = min(num_categories / 5, 1) * 10
    health_score = min(int(stock_score + avg_score + low_penalty + cat_score), 100)

    if health_score >= 80:
        health_label = "Excellent"
        score_color = "#22c55e"
        score_bg = "#14532d"
    elif health_score >= 60:
        health_label = "Good"
        score_color = "#eab308"
        score_bg = "#713f12"
    elif health_score >= 40:
        health_label = "Fair"
        score_color = "#f97316"
        score_bg = "#7c2d12"
    else:
        health_label = "Poor"
        score_color = "#ef4444"
        score_bg = "#7f1d1d"

    st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #112240, #1a3a5c);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
">
    <div style="display:grid; grid-template-columns:120px 1fr; gap:2rem; align-items:center;">
        <div style="text-align:center;">
            <div style="
                width:90px; height:90px;
                border-radius:50%;
                border: 3px solid {score_color};
                display:flex; flex-direction:column;
                align-items:center; justify-content:center;
                margin: 0 auto;
                background: {score_bg}33;
            ">
                <span style="font-size:28px; font-weight:600; color:{score_color};">{health_score}</span>
                <span style="font-size:10px; color:#64748b;">/ 100</span>
            </div>
            <p style="margin:8px 0 0; font-size:13px; font-weight:500; color:{score_color};">{health_label}</p>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px;">
            <div style="background:#14532d33; border:1px solid #22c55e44; border-radius:8px; padding:12px; text-align:center;">
                <p style="margin:0; font-size:20px; font-weight:600; color:#22c55e;">{in_stock}/{total}</p>
                <p style="margin:4px 0 0; font-size:11px; color:#86efac;">In stock</p>
            </div>
            <div style="background:#7f1d1d33; border:1px solid #ef444444; border-radius:8px; padding:12px; text-align:center;">
                <p style="margin:0; font-size:20px; font-weight:600; color:#ef4444;">{out_of_stock}</p>
                <p style="margin:4px 0 0; font-size:11px; color:#fca5a5;">Out of stock</p>
            </div>
            <div style="background:#78350f33; border:1px solid #f59e0b44; border-radius:8px; padding:12px; text-align:center;">
                <p style="margin:0; font-size:20px; font-weight:600; color:#f59e0b;">{low_stock_count}</p>
                <p style="margin:4px 0 0; font-size:11px; color:#fcd34d;">Low stock</p>
            </div>
            <div style="background:#1e3a5f33; border:1px solid #3b82f644; border-radius:8px; padding:12px; text-align:center;">
                <p style="margin:0; font-size:20px; font-weight:600; color:#60a5fa;">{num_categories}</p>
                <p style="margin:4px 0 0; font-size:11px; color:#93c5fd;">Categories</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── PRODUCTS TABLE ────────────────────────────────────────────
st.markdown("""
<p style="font-size:16px; font-weight:500; color:#90caf9; margin-bottom:1rem;">
    📋 Product Inventory
</p>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("No products found.")
else:
    display_df = df.drop(columns=["ID"]).copy()
    styled = style_table(display_df)
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.markdown("""
<div style="display:flex; gap:16px; margin-top:8px; font-size:12px;">
    <span style="display:flex; align-items:center; gap:6px;">
        <span style="background:#14532d; color:#86efac; padding:2px 8px; border-radius:4px; font-size:11px;">55</span>
        Good stock
    </span>
    <span style="display:flex; align-items:center; gap:6px;">
        <span style="background:#78350f; color:#fcd34d; padding:2px 8px; border-radius:4px; font-size:11px;">5</span>
        Low stock (&lt;10)
    </span>
    <span style="display:flex; align-items:center; gap:6px;">
        <span style="background:#7f1d1d; color:#fca5a5; padding:2px 8px; border-radius:4px; font-size:11px;">0</span>
        Out of stock
    </span>
</div>
""", unsafe_allow_html=True)
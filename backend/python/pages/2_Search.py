# pages/2_Search.py

import streamlit as st
import pandas as pd
import numpy as np
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
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Search", page_icon="🔍", layout="wide")

# ─── HELPER FUNCTIONS ──────────────────────────────────────────
@st.cache_resource
def load_model(model_name="all-MiniLM-L6-v2"):
    return SentenceTransformer(model_name)

@st.cache_data
def load_product_embeddings(model_name="all-MiniLM-L6-v2"):
    _model = load_model(model_name)
    all_products = list(Product.objects.all())
    texts, names, descriptions, categories, brands, prices, stocks = [], [], [], [], [], [], []

    for p in all_products:
        try:
            cat = p.category.title if p.category else ""
        except:
            cat = ""
        text = f"{p.name}. Category: {cat}. {p.description}"
        texts.append(text)
        names.append(p.name)
        descriptions.append(p.description)
        categories.append(cat)
        brands.append(p.brand)
        prices.append(float(str(p.price)))
        stocks.append(p.quantity_in_warehouse)

    embeddings = _model.encode(texts)
    return names, descriptions, categories, brands, prices, stocks, embeddings

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    mag = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return float(dot / mag) if mag != 0 else 0.0

def semantic_search(query, embeddings, names, top_k=5, model_name="all-MiniLM-L6-v2"):
    _model = load_model(model_name)
    query_vec = _model.encode([query])[0]
    scores = [(names[i], cosine_similarity(query_vec, embeddings[i])) for i in range(len(names))]
    scores.sort(key=lambda x: x[1], reverse=True)
    scores = [s for s in scores if s[1] >= 0.35]
    return scores[:top_k]

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

# ─── PAGE ──────────────────────────────────────────────────────
st.title("🔍 Search")
st.markdown("---")

df = get_all_products()

# ─── SEMANTIC SEARCH ───────────────────────────────────────────
st.subheader("🧠 Semantic Search")
st.markdown("Search products by **meaning** — not just keywords!")

semantic_query = st.text_input(
    "Search query",
    placeholder="e.g. 'wireless audio device', 'something to wear', 'mobile phone'"
)

if semantic_query:
    with st.spinner("🔍 Searching..."):
        names, descriptions, categories_list, brands, prices, stocks, embeddings = load_product_embeddings()
        results = semantic_search(semantic_query, embeddings, names, top_k=100)

    st.markdown(f"**Results for:** *'{semantic_query}'*")

    result_data = []
    for rank, (name, score) in enumerate(results, 1):
        idx = names.index(name)
        result_data.append({
            "Rank": rank,
            "Name": name,
            "Category": categories_list[idx],
            "Brand": brands[idx],
            "Price (₹)": prices[idx],
            "Stock": stocks[idx],
            "Similarity Score": round(score, 4)
        })

    result_df = pd.DataFrame(result_data)
    st.dataframe(result_df, use_container_width=True, hide_index=True)
    st.caption("💡 Similarity Score: closer to 1.0 = more relevant to your query")

st.markdown("---")

# ─── FIND SIMILAR PRODUCTS ─────────────────────────────────────
st.subheader("🔁 Find Similar Products")
st.markdown("Select any product and find the most similar items in your inventory!")

all_product_names = df["Name"].tolist() if not df.empty else []

if all_product_names:
    selected_product_name = st.selectbox(
        "Select a product",
        all_product_names,
        key="similar_product_select"
    )

    if st.button("🔍 Find Similar Products"):
        with st.spinner("Finding similar products..."):
            names, descriptions, categories_list, brands, prices, stocks, embeddings = load_product_embeddings()

            if selected_product_name in names:
                idx = names.index(selected_product_name)
                selected_vec = embeddings[idx]

                similarities = []
                for i, name in enumerate(names):
                    if name != selected_product_name:
                        score = cosine_similarity(selected_vec, embeddings[i])
                        similarities.append((name, score, i))

                similarities.sort(key=lambda x: x[1], reverse=True)
                similarities = [s for s in similarities if s[1] >= 0.5]
                top_similar = similarities[:50]

                st.markdown(f"**Products similar to:** *{selected_product_name}*")

                similar_data = []
                for rank, (name, score, i) in enumerate(top_similar, 1):
                    similar_data.append({
                        "Rank": rank,
                        "Name": name,
                        "Category": categories_list[i],
                        "Brand": brands[i],
                        "Price (₹)": prices[i],
                        "Stock": stocks[i],
                        "Similarity Score": round(score, 4)
                    })

                st.dataframe(
                    pd.DataFrame(similar_data),
                    use_container_width=True,
                    hide_index=True
                )
                st.caption("💡 Higher similarity score = more similar to your selected product")
            else:
                st.warning("Product not found in embeddings. Try refreshing!")
else:
    st.info("No products available.")
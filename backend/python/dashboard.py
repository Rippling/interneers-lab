# dashboard.py
# Streamlit dashboard for Product Inventory
# Run with: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add project root to path so we can import our models
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Connect to MongoDB
from db_connection import connect_to_mongodb
connect_to_mongodb()

# Import models directly
from products.models import Product
from products.category_model import ProductCategory

# ─── SEMANTIC SEARCH SETUP ─────────────────────────────────────
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_model(model_name="all-MiniLM-L6-v2"):
    """Load sentence transformer model — cached so it only loads once"""
    return SentenceTransformer(model_name)

@st.cache_data
def load_product_embeddings(model_name="all-MiniLM-L6-v2"):
    """Fetch all products and generate embeddings — cached"""
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
    """Search products by semantic similarity"""
    _model = load_model(model_name)
    query_vec = _model.encode([query])[0]
    scores = [(names[i], cosine_similarity(query_vec, embeddings[i])) for i in range(len(names))]
    scores.sort(key=lambda x: x[1], reverse=True)
    scores = [s for s in scores if s[1] >= 0.35]
    return scores[:top_k]

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="Product Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

# ─── TITLE ─────────────────────────────────────────────────────
st.title("📦 Product Inventory Dashboard")
st.markdown("---")

# ─── HELPER FUNCTIONS ──────────────────────────────────────────

def get_all_products():
    """Fetch all products from MongoDB"""
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
    """Fetch all categories from MongoDB"""
    return list(ProductCategory.objects.all())


# ─── SIDEBAR ───────────────────────────────────────────────────
st.sidebar.title("🔧 Controls")
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.subheader("Filter Products")
categories = get_all_categories()
category_options = ["All"] + [c.title for c in categories]
selected_category = st.sidebar.selectbox("Category", category_options)

brand_filter = st.sidebar.text_input("Brand contains")

st.sidebar.subheader("Price Range")
min_price = st.sidebar.number_input("Min Price", min_value=0, value=0)
max_price = st.sidebar.number_input("Max Price", min_value=0, value=1000000)

# ─── MAIN CONTENT ──────────────────────────────────────────────

df = get_all_products()

if not df.empty:
    if selected_category != "All":
        df = df[df["Category"] == selected_category]
    if brand_filter:
        df = df[df["Brand"].str.contains(brand_filter, case=False)]
    df = df[(df["Price (₹)"] >= min_price) & (df["Price (₹)"] <= max_price)]

# ─── METRICS ───────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", len(df))
with col2:
    total_stock = df["Stock"].sum() if not df.empty else 0
    st.metric("Total Stock", total_stock)
with col3:
    avg_price = round(df["Price (₹)"].mean(), 2) if not df.empty else 0
    st.metric("Avg Price", f"₹{avg_price}")
with col4:
    low_stock = len(df[df["Stock"] < 10]) if not df.empty else 0
    st.metric("Low Stock Items", low_stock)

st.markdown("---")

# ─── PRODUCTS TABLE ────────────────────────────────────────────
st.subheader("📋 Product Inventory")

if df.empty:
    st.warning("No products found. Add some products first!")
else:
    st.dataframe(
        df.drop(columns=["ID"]),
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

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

st.markdown("---")

# ─── CREATE CATEGORY ───────────────────────────────────────────
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

st.markdown("---")

# ─── SCENARIO SELECTOR ─────────────────────────────────────────
st.subheader("🎯 AI Scenario Selector")
st.markdown("Choose a warehouse scenario and let AI populate the database with relevant products!")

SCENARIOS = {
    "🎄 Holiday Rush": {
        "description": "Festive season — high demand for gifts, decorations, and party items",
        "stock_min": 300,
        "stock_max": 500,
        "prompt_hint": "festive holiday season products like gifts, decorations, party supplies, winter clothing, and electronics"
    },
    "☀️ Summer Collection": {
        "description": "Summer season — outdoor, cooling, and seasonal products",
        "stock_min": 200,
        "stock_max": 400,
        "prompt_hint": "summer season products like light clothing, outdoor gear, cooling appliances, summer foods and beverages"
    },
    "📚 Back to School": {
        "description": "School season — stationery, books, electronics, and essentials",
        "stock_min": 150,
        "stock_max": 350,
        "prompt_hint": "back to school products like books, stationery, bags, electronics like laptops and calculators, and school essentials"
    },
    "🎆 New Year Sale": {
        "description": "New Year — discounted items, party supplies, and fresh start products",
        "stock_min": 250,
        "stock_max": 450,
        "prompt_hint": "new year sale products like party supplies, fitness equipment, kitchen appliances, and lifestyle products"
    },
}

selected_scenario = st.selectbox("Select a Scenario", list(SCENARIOS.keys()))
scenario_info = SCENARIOS[selected_scenario]
st.info(f"📌 {scenario_info['description']}")
st.markdown(f"**Stock levels will be:** {scenario_info['stock_min']} – {scenario_info['stock_max']} units")
num_products = st.slider("How many products to generate?", min_value=5, max_value=30, value=10)

if st.button("🚀 Generate & Save Products", type="primary"):
    try:
        from groq import Groq
        from pydantic import BaseModel, field_validator
        from typing import Optional
        from datetime import datetime, timezone
        import json

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        all_categories = get_all_categories()
        category_map = {cat.title: cat for cat in all_categories}
        category_names = list(category_map.keys())

        prompt = f"""
Generate exactly {num_products} realistic warehouse products for a "{selected_scenario.replace('🎄 ', '').replace('☀️ ', '').replace('📚 ', '').replace('🎆 ', '')}" scenario as a JSON array.
Focus on: {scenario_info['prompt_hint']}
Each product must belong to one of these categories only: {category_names}
Each product must have exactly these fields:
- name: string
- description: string (1-2 sentences)
- category: string (must be exactly one of: {category_names})
- price: float (min 0.01)
- brand: string
- quantity_in_warehouse: integer (between {scenario_info['stock_min']} and {scenario_info['stock_max']})
Rules: Return ONLY a valid JSON array, no explanation, no markdown, no extra text
"""

        with st.spinner("🤖 AI is generating products..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

        raw_output = response.choices[0].message.content
        cleaned = raw_output.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        products_data = json.loads(cleaned)

        class ProductSchema(BaseModel):
            name: str
            description: Optional[str] = ""
            category: str
            price: float
            brand: str
            quantity_in_warehouse: int

            @field_validator('price')
            def price_must_be_positive(cls, v):
                if v <= 0:
                    raise ValueError("Price must be greater than 0")
                return round(v, 2)

            @field_validator('quantity_in_warehouse')
            def quantity_must_be_non_negative(cls, v):
                if v < 0:
                    raise ValueError("Quantity cannot be negative")
                return v

            @field_validator('category')
            def category_must_exist(cls, v):
                if v not in category_names:
                    raise ValueError(f"Invalid category: {v}")
                return v

        valid_products = []
        invalid_count = 0

        for product in products_data:
            try:
                validated = ProductSchema(**product)
                valid_products.append(validated)
            except Exception:
                invalid_count += 1

        saved = 0
        now = datetime.now(timezone.utc)

        for vp in valid_products:
            try:
                category_obj = category_map.get(vp.category)
                if not category_obj:
                    continue
                Product(
                    name=vp.name,
                    description=vp.description,
                    category=category_obj,
                    price=vp.price,
                    brand=vp.brand,
                    quantity_in_warehouse=vp.quantity_in_warehouse,
                    created_at=now,
                    updated_at=now
                ).save()
                saved += 1
            except Exception:
                invalid_count += 1

        st.success(f"🎉 Successfully saved {saved} products for '{selected_scenario}' scenario!")
        if invalid_count > 0:
            st.warning(f"⚠️ {invalid_count} products were skipped due to validation errors.")

        preview_data = [{"Name": vp.name, "Category": vp.category, "Brand": vp.brand,
                         "Price (₹)": vp.price, "Stock": vp.quantity_in_warehouse}
                        for vp in valid_products]
        st.dataframe(pd.DataFrame(preview_data), use_container_width=True, hide_index=True)
        st.info("🔄 Click 'Refresh Data' in the sidebar to see updated products!")

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")

st.markdown("---")

# ─── ASK THE EXPERT (RAG + MONGODB + LANGSMITH) ────────────────
st.subheader("🤖 Ask the Expert")
st.markdown("Ask anything about **warranties, return policies, stock levels, or vendor info** — powered by RAG + Live Database!")

# ── Langsmith setup (module level) ─────────────────────────────
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = "inventory-rag-week8"

from langsmith import traceable

# ── RAG Setup (cached) ─────────────────────────────────────────
@st.cache_resource
def setup_rag():
    """Load and chunk documents, embed and store in Chromadb — cached"""
    import chromadb
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    notebooks_path = Path(__file__).resolve().parent / "notebooks"

    files = {
        "product_manual": "product_manual.txt",
        "return_policy": "return_policy.txt",
        "vendor_faq": "vendor_faq.txt"
    }

    raw_docs = []
    for doc_name, filename in files.items():
        filepath = notebooks_path / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            raw_docs.append({"content": content, "source": doc_name})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )

    all_chunks = []
    for doc in raw_docs:
        chunks = splitter.split_text(doc["content"])
        for chunk in chunks:
            all_chunks.append({"text": chunk, "source": doc["source"]})

    rag_model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [c["text"] for c in all_chunks]
    sources = [c["source"] for c in all_chunks]
    embeddings = rag_model.encode(texts).tolist()

    chroma_client = chromadb.Client()
    try:
        chroma_client.delete_collection("inventory_docs")
    except:
        pass

    collection = chroma_client.create_collection("inventory_docs")
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": s} for s in sources],
        ids=[f"chunk_{i}" for i in range(len(all_chunks))]
    )

    return collection, rag_model

# ── Traceable functions ─────────────────────────────────────────
@traceable(name="retrieve_chunks")
def retrieve_chunks(query, collection, rag_model, top_k=3):
    """Retrieve relevant chunks from Chromadb"""
    query_vec = rag_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_vec, n_results=top_k)
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"]
        })
    return chunks

@traceable(name="mongodb_product_lookup")
def lookup_products_in_db(question):
    """Search MongoDB for products mentioned in the question"""
    all_products = list(Product.objects.all())
    matched = []
    q_lower = question.lower()
    q_words = [w for w in q_lower.split() if len(w) > 2]  # ← fixed: min 2 chars not 3

    for p in all_products:
        product_name_lower = p.name.lower()
        # Match if ANY word from question appears in product name
        if any(word in product_name_lower for word in q_words):
            try:
                cat = p.category.title if p.category else "Unknown"
            except:
                cat = "Unknown"
            matched.append({
                "name": p.name,
                "brand": p.brand,
                "category": cat,
                "price": float(str(p.price)),
                "stock": p.quantity_in_warehouse
            })

    return matched[:5]

@traceable(name="ask_expert", run_type="chain")
def ask_expert(question, collection, rag_model):
    """
    Combined RAG + MongoDB pipeline with Langsmith tracing:
    1. Retrieve relevant doc chunks
    2. Lookup matching products in MongoDB
    3. Build combined prompt
    4. Send to Groq
    5. Return grounded answer
    """
    from groq import Groq

    # Step 1 — Retrieve doc chunks
    chunks = retrieve_chunks(question, collection, rag_model, top_k=3)
    doc_context = "\n\n".join([f"[{c['source']}]: {c['text']}" for c in chunks])

    # Step 2 — Lookup MongoDB
    matched_products = lookup_products_in_db(question)

    if matched_products:
        db_context = "Live inventory data from database:\n"
        for p in matched_products:
            status = "IN STOCK" if p["stock"] > 0 else "OUT OF STOCK"
            db_context += (
                f"- {p['name']} ({p['brand']}) | "
                f"Category: {p['category']} | "
                f"Price: ₹{p['price']} | "
                f"Stock: {p['stock']} units ({status})\n"
            )
    else:
        db_context = "No matching products found in live database for this query."

    # Step 3 — Build combined prompt
    prompt = f"""You are an expert assistant for a product inventory system.
You have access to two sources of information:
1. Documentation (warranties, return policies, vendor FAQ)
2. Live database (current stock levels, prices)

Answer the user's question using BOTH sources below.
If stock info is available, always mention current stock levels.
If warranty or policy info is available, always include it.
Only use information from the sources provided — do not make anything up.
If the answer is not in either source, say "I don't have information about this."

--- DOCUMENTATION ---
{doc_context}

--- LIVE DATABASE ---
{db_context}

Question: {question}

Answer:"""

    # Step 4 — Send to Groq
    @traceable(name="groq_llm_call", run_type="llm")
    def call_groq(messages):
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.1
        )
        return response.choices[0].message.content

    answer = call_groq([{"role": "user", "content": prompt}])

    return answer, chunks, matched_products

# ── Chat Interface ──────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.spinner("⏳ Loading knowledge base..."):
    try:
        collection, rag_model = setup_rag()
        rag_ready = True
    except Exception as e:
        st.error(f"❌ Could not load knowledge base: {e}")
        rag_ready = False

if rag_ready:
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("📄 Doc sources used"):
                    for chunk in chat["chunks"]:
                        st.caption(f"[{chunk['source']}] {chunk['text'][:200]}...")
            with col2:
                with st.expander("🗄️ Live DB data used"):
                    if chat["products"]:
                        for p in chat["products"]:
                            status = "✅ In Stock" if p["stock"] > 0 else "❌ Out of Stock"
                            st.caption(f"{p['name']} — {p['stock']} units {status}")
                    else:
                        st.caption("No matching products found in DB")

    # Chat input
    user_question = st.chat_input(
        "Ask anything — e.g. 'Is iPhone 14 in stock and what is its warranty?'"
    )

    if user_question:
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching docs + live database..."):
                try:
                    answer, chunks, products = ask_expert(
                        user_question, collection, rag_model
                    )
                    st.write(answer)

                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander("📄 Doc sources used"):
                            for chunk in chunks:
                                st.caption(f"[{chunk['source']}] {chunk['text'][:200]}...")
                    with col2:
                        with st.expander("🗄️ Live DB data used"):
                            if products:
                                for p in products:
                                    status = "✅ In Stock" if p["stock"] > 0 else "❌ Out of Stock"
                                    st.caption(f"{p['name']} — {p['stock']} units {status}")
                            else:
                                st.caption("No matching products found in DB")

                    st.session_state.chat_history.append({
                        "question": user_question,
                        "answer": answer,
                        "chunks": chunks,
                        "products": products
                    })
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    st.caption("💡 Answers combine live stock data from MongoDB + warranty/policy info from documents.")
    st.caption("🔭 All queries are traced in Langsmith under inventory-rag-week8 project.")

    st.markdown("---")

# ─── QUOTE AGENT ───────────────────────────────────────────────
st.subheader("💰 AI Quote Agent")
st.markdown("Get instant quotes for any product — with automatic bulk discounts!")

# ── Quote Agent Setup ───────────────────────────────────────────
def find_product(product_name: str):
    """Smart product search — handles plural, case, partial names"""
    product = Product.objects(name__icontains=product_name).first()
    if product:
        return product
    product = Product.objects(name__icontains=product_name[:-1]).first()
    if product:
        return product
    first_word = product_name.split()[0]
    product = Product.objects(name__icontains=first_word).first()
    return product

def get_product_info(product_name: str) -> dict:
    product = find_product(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found"}
    try:
        category = product.category.title if product.category else "Unknown"
    except:
        category = "Unknown"
    return {
        "product_id": str(product.id),
        "name": product.name,
        "brand": product.brand,
        "category": category,
        "price": float(str(product.price)),
        "description": product.description
    }

def check_inventory(product_name: str) -> dict:
    product = find_product(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found"}
    stock = product.quantity_in_warehouse
    if stock == 0:
        status = "OUT OF STOCK"
    elif stock < 10:
        status = "LOW STOCK"
    elif stock < 50:
        status = "IN STOCK"
    else:
        status = "WELL STOCKED"
    return {
        "product_id": str(product.id),
        "name": product.name,
        "stock": stock,
        "status": status,
        "can_fulfill": stock > 0
    }

def calculate_quote(product_name: str, quantity: int) -> dict:
    MAX_DISCOUNT = 20.0
    product = find_product(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found"}
    stock = product.quantity_in_warehouse
    if stock < quantity:
        return {"error": f"Insufficient stock. Requested: {quantity}, Available: {stock}"}
    unit_price = float(str(product.price))
    if quantity <= 10:
        discount_pct = 0
        discount_reason = "No discount for small orders"
    elif quantity <= 50:
        discount_pct = 10
        discount_reason = "10% bulk discount for orders of 11-50 units"
    else:
        discount_pct = MAX_DISCOUNT
        discount_reason = "20% bulk discount for orders of 51+ units"
    original_total = unit_price * quantity
    discount_amount = original_total * (discount_pct / 100)
    final_total = original_total - discount_amount
    return {
        "product_name": product.name,
        "brand": product.brand,
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "discount_percentage": discount_pct,
        "discount_reason": discount_reason,
        "original_total": round(original_total, 2),
        "discount_amount": round(discount_amount, 2),
        "final_total": round(final_total, 2),
        "currency": "INR",
        "policy_override": False
    }

QUOTE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_product_info",
            "description": "Get product details like price, brand, and category from inventory",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name or partial name of the product"
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Check how many units of a product are currently in stock",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product to check inventory for"
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_quote",
            "description": "Calculate total price quote with bulk discounts applied",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of units requested"
                    }
                },
                "required": ["product_name", "quantity"]
            }
        }
    }
]

QUOTE_TOOL_MAP = {
    "get_product_info": get_product_info,
    "check_inventory": check_inventory,
    "calculate_quote": calculate_quote
}

def run_quote_agent_dashboard(user_request: str) -> tuple:
    """Run quote agent and return answer + tool call log"""
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": """You are a Quote Agent for a product inventory system.
When a user asks for a product quote, you must:
1. Find the product using get_product_info
2. Check stock using check_inventory
3. Calculate the quote using calculate_quote
4. Return a clear, friendly quote summary with all pricing details

Always use all 3 tools before giving final answer.
Mention discount if applicable. Be friendly and professional."""
        },
        {"role": "user", "content": user_request}
    ]

    tool_log = []
    step = 1
    max_retries = 3

    while True:
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    tools=QUOTE_TOOLS,
                    tool_choice="auto"
                )
                break
            except Exception as e:
                if "tool_use_failed" in str(e) and attempt < max_retries - 1:
                    continue
                else:
                    return f"Error: {str(e)}", tool_log

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content, tool_log

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_result = QUOTE_TOOL_MAP[tool_name](**tool_args)

            tool_log.append({
                "tool": tool_name,
                "args": tool_args,
                "result": tool_result
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

        step += 1
        if step > 10:
            return "Agent exceeded maximum steps", tool_log

# ── Quote Chat Interface ────────────────────────────────────────
if "quote_history" not in st.session_state:
    st.session_state.quote_history = []

# Display discount rules
col1, col2, col3 = st.columns(3)
with col1:
    st.info("📦 1-10 units → No discount")
with col2:
    st.info("📦 11-50 units → 10% off")
with col3:
    st.info("📦 51+ units → 20% off (max)")

# Display chat history
for chat in st.session_state.quote_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.write(chat["answer"])
        with st.expander("🔧 Tools called by Agent"):
            for log in chat["tool_log"]:
                st.caption(f"🔧 {log['tool']}({log['args']})")
                st.caption(f"📤 Result: {log['result']}")
                st.markdown("---")

# Chat input
quote_question = st.text_input(
    "Ask for a quote",
    placeholder="e.g. 'I need 60 Coffee Makers, any deal?'",
    key="quote_input"
)
get_quote_btn = st.button("🤖 Get Quote", type="primary")

if get_quote_btn and quote_question:
    with st.chat_message("user"):
        st.write(quote_question)
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agent is working on your quote..."):
            try:
                answer, tool_log = run_quote_agent_dashboard(quote_question)
                st.write(answer)
                with st.expander("🔧 Tools called by Agent"):
                    for log in tool_log:
                        st.caption(f"🔧 {log['tool']}({log['args']})")
                        st.caption(f"📤 Result: {log['result']}")
                        st.markdown("---")
                st.session_state.quote_history.append({
                    "question": quote_question,
                    "answer": answer,
                    "tool_log": tool_log
                })
            except Exception as e:
                st.error(f"❌ Error: {e}")

if st.session_state.quote_history:
    if st.button("🗑️ Clear Quote History", key="clear_quote"):
        st.session_state.quote_history = []
        st.rerun()

st.caption("💡 Discount rules: 1-10 units = 0%, 11-50 units = 10%, 51+ units = 20% (max allowed by policy)")
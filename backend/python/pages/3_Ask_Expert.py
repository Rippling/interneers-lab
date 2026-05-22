# pages/3_Ask_Expert.py

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
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Ask the Expert", page_icon="🤖", layout="wide")

# ── Langsmith setup ─────────────────────────────────────────────
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = "inventory-rag-week8"

from langsmith import traceable

# ── RAG Setup (cached) ─────────────────────────────────────────
@st.cache_resource
def setup_rag():
    import chromadb
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    notebooks_path = Path(__file__).resolve().parent.parent / "notebooks"

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

@traceable(name="retrieve_chunks")
def retrieve_chunks(query, collection, rag_model, top_k=3):
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
    all_products = list(Product.objects.all())
    matched = []
    q_lower = question.lower()
    q_words = [w for w in q_lower.split() if len(w) > 2]

    for p in all_products:
        product_name_lower = p.name.lower()
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
    from groq import Groq

    chunks = retrieve_chunks(question, collection, rag_model, top_k=3)
    doc_context = "\n\n".join([f"[{c['source']}]: {c['text']}" for c in chunks])

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

# ─── PAGE ──────────────────────────────────────────────────────
st.title("🤖 Ask the Expert")
st.markdown("Ask anything about **warranties, return policies, stock levels, or vendor info** — powered by RAG + Live Database!")
st.markdown("---")

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

    user_question = st.text_input(
        "Ask the Expert",
        placeholder="e.g. 'Is iPhone 14 in stock and what is its warranty?'",
        key="expert_input"
    )
    ask_expert_btn = st.button("🤖 Ask Expert", type="primary")

    if ask_expert_btn and user_question:
        with st.chat_message("user"):
            st.write(user_question)
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching docs + live database..."):
                try:
                    answer, chunks, products = ask_expert(user_question, collection, rag_model)
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
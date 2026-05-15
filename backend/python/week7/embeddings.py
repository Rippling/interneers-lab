# this files takes product data or query text and convert it to embeddings
# it prepares the vector representation needed
from functools import lru_cache
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from week4.db_connection import initialize_mongo
from week4.models import Product


def initiate_db_connection():
    initialize_mongo()


# this func loads the model, loading is expensive, hence with cache: model loads first time and next time same model is reused for search, query and comparision
# it can remember 4 models at one time, although we require only 1 all-MiniLM-L6-v2
@lru_cache(maxsize=4)
def load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    # sentence transformer loads SBERT style models like all-MiniLM-L6-v2, all-mpnet-base-v2
    return SentenceTransformer(model_name)


# converts one product object into one text string bcz embedding models take text input not raw databse objects
def build_product_text(product) -> str:
    parts = []
    if product.name:
        parts.append(product.name)
    if product.description:
        parts.append(product.description)
    if product.brand:
        parts.append(product.brand)
    if product.category and product.category.title:
        parts.append(product.category.title)
    return " | ".join(parts)


# fetches all products from mongoDB by category
def fetch_products_by_category(selected_category_id=None) -> List:
    initiate_db_connection()
    if selected_category_id is None:
        return list(Product.objects().order_by("id"))
    else:
        return list(Product.objects(category=selected_category_id).order_by("id"))


# converts raw mongoDB product objects into python dict
def build_product_records(products: List) -> List[Dict[str, Any]]:
    records = []
    for product in products:
        records.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "brand": product.brand,
            "price": float(product.price),
            "quantity": product.quantity,
            "category": product.category.title if product.category else "No Category",
            "text": build_product_text(product),
        })
    return records


def generate_embeddings_for_texts(texts: List[str], model_name: str = "all-MiniLM-L6-v2"):
    model = load_embedding_model(model_name)
    return model.encode(texts, convert_to_numpy=True)


# 1. fetch products from DB
# 2. convert them into clean records
# 3. extract text from each record
# 4. generate embeddings
def get_product_records_and_embeddings(selected_category_id=None, model_name: str = "all-MiniLM-L6-v2"):
    products = fetch_products_by_category(selected_category_id)
    records = build_product_records(products)
    if not records:
        return [], None
    texts = []
    for record in records:
        texts.append(record["text"])
    embeddings = generate_embeddings_for_texts(texts, model_name=model_name)
    return records, embeddings


def generate_query_embedding(query: str, model_name: str = "all-MiniLM-L6-v2"):
    model = load_embedding_model(model_name)
    return model.encode(query, convert_to_numpy=True)

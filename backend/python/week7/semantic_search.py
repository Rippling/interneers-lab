import numpy as np
from week7.embeddings import get_product_records_and_embeddings, generate_query_embedding


def cosine_similarity_manually(vec1, vec2) -> float:
    vec1 = np.array(vec1, dtype=float)
    vec2 = np.array(vec2, dtype=float)

    # computing magnitude
    vec1_norm = np.linalg.norm(vec1)
    vec2_norm = np.linalg.norm(vec2)

    if vec1_norm == 0 or vec2_norm == 0:
        return 0.0

    # cosine similarity formula
    similarity = np.dot(vec1, vec2) / (vec1_norm * vec2_norm)
    return float(similarity)


# take a user search query and return top k most semantically similar products
def semantic_search(query: str, top_k: int = 5, model_name: str = "all-MiniLM-L6-v2", selected_category_id=None):
    if not query or not query.strip():
        return []

    product_records, product_embeddings = get_product_records_and_embeddings(
        selected_category_id=selected_category_id,
        model_name=model_name
    )

    if not product_records or product_embeddings is None:
        return []

    query_embedding = generate_query_embedding(
        query=query.strip(),
        model_name=model_name
    )

    scored_results = []

    # record gives product info and index gives access to matching embedding
    # record = product_records[index] and embedding = product_embeddings[index]
    for index, record in enumerate(product_records):
        score = cosine_similarity_manually(
            query_embedding,
            product_embeddings[index]
        )

        scored_results.append({
            "id": record["id"],
            "name": record["name"],
            "description": record["description"],
            "brand": record["brand"],
            "price": record["price"],
            "quantity": record["quantity"],
            "category": record["category"],
            "semantic_score": round(score, 6),
        })

    scored_results.sort(key=lambda x: x["semantic_score"], reverse=True)
    return scored_results[:top_k]


def find_similar_products(product_id: int, top_k: int = 5, model_name: str = "all-MiniLM-L6-v2"):
    product_records, product_embeddings = get_product_records_and_embeddings(
        selected_category_id=None,
        model_name=model_name
    )

    if not product_records or product_embeddings is None:
        return []

    target_index = None

    for index, record in enumerate(product_records):
        if record["id"] == product_id:
            target_index = index
            break

    if target_index is None:
        return []

    target_embedding = product_embeddings[target_index]
    scored_results = []

    for index, record in enumerate(product_records):
        if record["id"] == product_id:
            continue

        score = cosine_similarity_manually(
            target_embedding,
            product_embeddings[index]
        )

        scored_results.append({
            "id": record["id"],
            "name": record["name"],
            "description": record["description"],
            "brand": record["brand"],
            "price": record["price"],
            "quantity": record["quantity"],
            "category": record["category"],
            "semantic_score": round(score, 6),
        })

    scored_results.sort(key=lambda x: x["semantic_score"], reverse=True)
    return scored_results[:top_k]

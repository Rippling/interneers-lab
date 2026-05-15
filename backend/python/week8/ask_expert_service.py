# this file is also for adv task, it combines rag pipelines and stock lookup
from week8.rag_pipeline import run_rag_pipeline
from week8.stock_lookup import get_product_stock
from week8.config import DEFAULT_TOP_K

# it helps in answering questions like : "is car in stock and what is the warranty?"


def ask_expert(user_query, product_name: str | None = None, top_k: int = DEFAULT_TOP_K):
    rag_result = run_rag_pipeline(user_query, top_k=top_k)
    stock_result = None
    if product_name:
        stock_result = get_product_stock(product_name)
    final_answer = rag_result["answer"]
    if stock_result:
        stock_text = (
            f"\n\nCurrent Stock Information:\n"
            f"- Product: {stock_result['name']}\n"
            f"- Brand: {stock_result['brand']}\n"
            f"- Category: {stock_result['category']}\n"
            f"- Price: {stock_result['price']}\n"
            f"- Quantity Available: {stock_result['quantity']}"
        )
        final_answer += stock_text
    return {
        "query": user_query,
        "answer": final_answer,
        "rag_answer": rag_result["answer"],
        "rag_prompt": rag_result["prompt"],
        "retrieved_chunks": rag_result["retrieved_chunks"],
        "stock_result": stock_result,
    }


if __name__ == "__main__":
    user_query = input("Enter your question: ").strip()
    product_name = input(
        "Enter product name for stock lookup (or press Enter to skip): ").strip()
    if not user_query:
        print("No query entered.")
    else:
        result = ask_expert(
            user_query=user_query, product_name=product_name if product_name else None, top_k=DEFAULT_TOP_K)
        print("\nFinal Answer:")
        print(result["answer"])

        print("\nRetrieved Chunks:")
        for index, chunk in enumerate(result["retrieved_chunks"], start=1):
            print("=" * 80)
            print(f"Result #{index}")
            print(f"Source: {chunk['source']}")
            print(f"Title: {chunk['title']}")
            print(f"Chunk Index: {chunk['chunk_index']}")
            print(chunk["text"])

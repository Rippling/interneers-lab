from week8.prompt_builder import build_rag_prompt
from week8.retriever import retrieve_relavant_chunks
from week8.llm_client import generate_answer
from week8.config import DEFAULT_TOP_K
from langsmith import traceable
from week8.langsmith_setup import setup_langsmith_tracing

setup_langsmith_tracing()


@traceable(run_type="chain", name="week8_rag_pipeline")
def run_rag_pipeline(user_query, top_k: int = DEFAULT_TOP_K):
    retrieved_chunks = retrieve_relavant_chunks(user_query, top_k=top_k)
    prompt = build_rag_prompt(user_query, retrieved_chunks)
    answer = generate_answer(prompt)
    return {
        "query": user_query,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks,
        "prompt": prompt
    }


if __name__ == "__main__":
    query = input("Enter your question: ").strip()
    if not query:
        print("No query entered.")
    else:
        result = run_rag_pipeline(query)
        print(f"Query: {result['query']}\n")
        print(f"Answer: {result['answer']}\n")
        print("\nRetrieved Chunks:")
        for index, chunk in enumerate(result["retrieved_chunks"], start=1):
            print("=" * 80)
            print(f"Result #{index}")
            print(f"Source: {chunk['source']}")
            print(f"Title: {chunk['title']}")
            print(f"Chunk Index: {chunk['chunk_index']}")
            print(chunk["text"])

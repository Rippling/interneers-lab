from week8.vector_store import search_similar_chunks
from week8.config import DEFAULT_TOP_K
from langsmith import traceable


@traceable(run_type="retriever", name="week8_retrieve_relevant_chunks")
def retrieve_relavant_chunks(query, top_k: int = DEFAULT_TOP_K):
    results = search_similar_chunks(query, top_k)
    retrieved_chunks = []
    for doc in results:
        retrieved_chunks.append(
            {
                "text": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "doc_type": doc.metadata.get("doc_type", "unknown"),
                "title": doc.metadata.get("title", "Unknown"),
                "chunk_index": doc.metadata.get("chunk_index", -1),
            }
        )
    return retrieved_chunks


if __name__ == "__main__":
    query = "What's the return policy for damaged items?"
    chunks = retrieve_relavant_chunks(query)
    print(f"Query: {query}\n")
    for index, chunk in enumerate(chunks, start=1):
        print("=" * 80)
        print(f"Result #{index}")
        print(f"Source: {chunk['source']}")
        print(f"Title: {chunk['title']}")
        print(f"Doc Type: {chunk['doc_type']}")
        print(f"Chunk Index: {chunk['chunk_index']}")
        print("Text:")
        print(chunk["text"])
        print()

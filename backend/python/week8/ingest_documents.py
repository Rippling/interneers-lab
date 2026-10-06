# it connects knowlege_base, text_chunker, vector_store
from week8.knowledge_base import load_text_documents, list_available_sources
from week8.text_chunker import split_documents
from week8.vector_store import index_documents

# 1. load the source file
# 2. split them into chunks
# 3. store those chunks in chromaDB


def ingest_knowledge_base():
    documents = load_text_documents()
    chunked_documents = split_documents(documents)
    vector_store = index_documents(chunked_documents)
    return {
        "source_files": list_available_sources(),
        "document_count": len(documents),
        "chunk_count": len(chunked_documents),
        "vector_store": vector_store,
    }


if __name__ == "__main__":
    result = ingest_knowledge_base()
    print("Knowledge base ingestion completed.")
    print(f"Source files: {result['source_files']}")
    print(f"Loaded documents: {result['document_count']}")
    print(f"Created chunks: {result['chunk_count']}")

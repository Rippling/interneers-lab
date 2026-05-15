# this file is the bridge between chunked texts and searchable semantic retrieval
from functools import lru_cache
from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer
from week8.config import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR, EMBEDDING_MODEL_NAME, DEFAULT_TOP_K

# 1. it connects chunked document to chromaDB
# 2. it gives a way to search similar chunks


@lru_cache(maxsize=1)
def load_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


# this class converts plain sentencetransformer model into langchain compatible embedding object
class LocalSentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = load_embedding_model()
        self.model_name = model_name

    def embed_documents(self, texts: list[str]):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, text):
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()


# creates or loads chroma vector store
def get_vector_store(persist_directory: Path = CHROMA_PERSIST_DIR):
    persist_directory.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=str(persist_directory),
        embedding_function=LocalSentenceTransformerEmbeddings(),
    )


# takes chunked documents and adds them to chroma.db
def index_documents(documents: list[Document]):
    vector_store = get_vector_store()
    vector_store.add_documents(documents)
    return vector_store


# searches the vector using a user query
def search_similar_chunks(query: str, top_k: int = DEFAULT_TOP_K):
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=top_k)

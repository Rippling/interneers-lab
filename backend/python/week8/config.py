# central setting file for week 8
# it keeps all fixed value of the project in one place
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"
CHROMA_COLLECTION_NAME = "week8_inventory_knowledge"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 700
CHUNK_OVERLAP = 120
CHUNK_OVERLAP = 120
DEFAULT_TOP_K = 3
GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_TEMPERATURE = 0.2
TRACING_PROJECT_NAME = "interneers-lab-week8"
DOCUMENT_FILE_MAP = {
    "product_manual.txt": {
        "doc_type": "product_manual",
        "title": "Product Manual",
    },
    "return_policy.txt": {
        "doc_type": "return_policy",
        "title": "Return Policy",
    },
    "vendor_faq.txt": {
        "doc_type": "vendor_faq",
        "title": "Vendor FAQ",
    },
}

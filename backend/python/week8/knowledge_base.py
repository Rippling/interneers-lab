# this file loads the source doc in a clean, structured way before chunkuing
from pathlib import Path
from langchain_core.documents import Document
from week8.config import DATA_DIR, DOCUMENT_FILE_MAP


# 1. go to week8/data
# 2. find all .txt files
# 3. read their content
# 4. attach metadata
# 5. returns them in a structured format


# loads .txt files from week8/data and returns a list of langchain document object
def load_text_documents(data_dir: Path = DATA_DIR):
    documents = []

    for file_path in sorted(data_dir.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()
        if not text:
            continue

        doc_info = DOCUMENT_FILE_MAP.get(
            file_path.name,
            {
                "doc_type": "generic_text",
                "title": file_path.stem.replace("_", " ").title(),
            },
        )
        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name,
                    "doc_type": doc_info["doc_type"],
                    "title": doc_info["title"],
                },
            )
        )

    return documents


# return the name of .txt file available
def list_available_sources(data_dir: Path = DATA_DIR):
    sources = []
    for file_path in sorted(data_dir.glob("*.txt")):
        sources.append(file_path.name)
    return sources

from week8.knowledge_base import load_text_documents
from week8.text_chunker import split_documents

documents = load_text_documents()
chunks = split_documents(documents)

print("Total chunks:", len(chunks))
print()

for chunk in chunks:
    print("=" * 80)
    print("SOURCE:", chunk.metadata["source"])
    print("DOC TYPE:", chunk.metadata["doc_type"])
    print("TITLE:", chunk.metadata["title"])
    print("CHUNK INDEX:", chunk.metadata["chunk_index"])
    print("TEXT:")
    print(chunk.page_content)
    print()

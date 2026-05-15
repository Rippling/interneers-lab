# knowledeg_base loads full document
# now this file will break them into pieces
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from week8.config import CHUNK_SIZE, CHUNK_OVERLAP

# RecursiveCharacterTextSplitter takes long documents and split them into smaller pieces, preserves metadata while splitting


def split_documents(documents: list[Document]):
    # try splliting by para, if needed split by line, if needed split by sentence boundarym, if needed split by word spaces, if nothing works split by character wise
    # here we are just setting the rules that how to split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, separators=[
            "\n\n", "\n", ". ", " ", ""]
    )
    # this gives call to split text
    split_docs = text_splitter.split_documents(documents)
    for index, doc in enumerate(split_docs):
        doc.metadata["chunk_index"] = index + 1
    return split_docs

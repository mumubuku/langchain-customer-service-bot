import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(doc_dir):
    loader = DirectoryLoader(doc_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)


def get_latest_doc_timestamp(doc_dir):
    paths = Path(doc_dir).rglob("*.pdf")
    return max((p.stat().st_mtime for p in paths), default=0.0)


def list_documents(doc_dir):
    paths = Path(doc_dir).rglob("*.pdf")
    return [
        {
            "filename": str(p.name),
            "size": p.stat().st_size,
            "mtime": p.stat().st_mtime
        }
        for p in paths
    ]


def delete_document(doc_dir, filename):
    path = Path(doc_dir) / filename
    if path.exists() and path.suffix == ".pdf":
        path.unlink()
        return True
    return False

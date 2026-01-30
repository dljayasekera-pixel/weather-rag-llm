"""
RAG service: load knowledge base, build vector store, retrieve relevant chunks for a query.
Uses sentence-transformers (local) and ChromaDB so it works without OpenAI.
"""

import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Default paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge_base"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"


def get_embeddings():
    """Local embeddings (no API key)."""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )


def load_and_index_knowledge(persist_directory: str = None, force_rebuild: bool = False) -> Chroma:
    """Load markdown/text from knowledge_base, split, embed, and store in Chroma."""
    persist_directory = persist_directory or str(CHROMA_DIR)
    if not force_rebuild and os.path.isdir(persist_directory):
        try:
            return Chroma(
                persist_directory=persist_directory,
                embedding_function=get_embeddings(),
            )
        except Exception:
            pass
    loader = DirectoryLoader(
        str(KNOWLEDGE_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"autodetect_encoding": True},
    )
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    splits = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=get_embeddings(),
        persist_directory=persist_directory,
    )
    vectorstore.persist()
    return vectorstore


def retrieve_context(query: str, vectorstore: Chroma, k: int = 4) -> str:
    """Return concatenated context from top-k similar chunks."""
    if vectorstore is None:
        return ""
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join(d.page_content for d in docs)

from loader import load_documents
from chunker import create_chunks

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load documents
docs = load_documents()

# Create chunks
chunks = create_chunks(docs)

print("Chunks Created:", len(chunks))

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Store in ChromaDB
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)

print("ChromaDB Created Successfully")
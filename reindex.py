import shutil
import os

from loader import load_documents
from chunker import create_chunks

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Delete old ChromaDB
if os.path.exists("chroma_db"):
    shutil.rmtree("chroma_db")
    print("Old ChromaDB deleted")

# Reload documents
docs = load_documents()

# Recreate chunks
chunks = create_chunks(docs)

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Rebuild ChromaDB
db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)

print("Reindexing Completed Successfully")
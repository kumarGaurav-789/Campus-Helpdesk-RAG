from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Same embedding model used during indexing
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load existing ChromaDB
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)

query = input("Ask a Question: ")

results = db.similarity_search(query, k=1)

print("\nTop Results:\n")

for i, doc in enumerate(results):
    print(f"\nResult {i+1}")
    print(doc.page_content)
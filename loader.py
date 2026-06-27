import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader
)

def load_documents():
    documents = []

    for file in os.listdir("documents"):

        path = os.path.join("documents", file)

        try:
            if file.endswith(".pdf"):
                loader = PyPDFLoader(path)

            elif file.endswith(".docx"):
                loader = Docx2txtLoader(path)

            else:
                continue

            docs = loader.load()
            documents.extend(docs)

            print(f"Loaded: {file}")

        except Exception as e:
            print(f"Skipped {file} -> {e}")

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"\nTotal pages loaded: {len(docs)}")

    for doc in docs[:3]:
        print("\n--- PAGE ---")
        print(doc.page_content[:300])
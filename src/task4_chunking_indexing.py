import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_documents():
    docs = []
    base_dir = Path("data/standardized")
    for file_path in base_dir.rglob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        docs.append({
            "content": content,
            "metadata": {
                "source": file_path.name,
                "type": file_path.parent.name
            }
        })
    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = []
    for doc in docs:
        splits = splitter.split_text(doc["content"])
        for split in splits:
            chunks.append({
                "content": split,
                "metadata": doc["metadata"]
            })
    return chunks

def index_documents(chunks):
    import chromadb
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="rag_docs")
    
    # clear existing docs
    if collection.count() > 0:
        collection.delete(collection.get()["ids"])
        
    if not chunks:
        return
        
    docs_text = [c["content"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [f"id_{i}" for i in range(len(chunks))]
    
    collection.add(
        documents=docs_text,
        metadatas=metadatas,
        ids=ids
    )

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    index_documents(chunks)
    print("Indexed documents successfully!")

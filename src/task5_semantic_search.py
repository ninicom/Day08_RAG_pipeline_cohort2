import chromadb

def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        collection = client.get_or_create_collection(name="rag_docs")
    except Exception:
        return []
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=['documents', 'metadatas', 'distances']
    )
    
    formatted_results = []
    if results['documents'] and results['documents'][0]:
        for i in range(len(results['documents'][0])):
            score = 1.0 / (1.0 + results['distances'][0][i])
            formatted_results.append({
                "content": results['documents'][0][i],
                "score": score,
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
            })
            
    formatted_results.sort(key=lambda x: x['score'], reverse=True)
    return formatted_results

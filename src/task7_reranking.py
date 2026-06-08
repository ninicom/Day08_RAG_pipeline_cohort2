from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    if not candidates:
        return []
        
    model = get_model()
    query_emb = model.encode(query)
    
    docs = [c["content"] for c in candidates]
    doc_embs = model.encode(docs)
    
    scores = util.cos_sim(query_emb, doc_embs)[0].tolist()
    
    results = []
    for i, c in enumerate(candidates):
        results.append({
            "content": c["content"],
            "score": scores[i],
            "metadata": c.get("metadata", {})
        })
        
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

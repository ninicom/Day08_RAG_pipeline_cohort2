from rank_bm25 import BM25Okapi

def load_chunks():
    from src.task4_chunking_indexing import load_documents, chunk_documents
    docs = load_documents()
    return chunk_documents(docs)

_chunks = None
_bm25 = None

def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    global _chunks, _bm25
    if _chunks is None:
        _chunks = load_chunks()
        tokenized_corpus = [c["content"].lower().split() for c in _chunks]
        if tokenized_corpus:
            _bm25 = BM25Okapi(tokenized_corpus)
            
    if not _bm25 or not _chunks:
        return []
        
    tokenized_query = query.lower().split()
    scores = _bm25.get_scores(tokenized_query)
    
    results = []
    for i, score in enumerate(scores):
        if score > 0:
            results.append({
                "content": _chunks[i]["content"],
                "score": score,
                "metadata": _chunks[i]["metadata"]
            })
            
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

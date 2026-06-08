from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search
from src.task7_reranking import rerank
from src.task8_pageindex_vectorless import pageindex_search

def retrieve(query: str, top_k: int = 5, score_threshold: float = 0.3) -> list[dict]:
    semantic_results = semantic_search(query, top_k=top_k*2)
    lexical_results = lexical_search(query, top_k=top_k*2)
    
    merged = {}
    for i, r in enumerate(semantic_results):
        merged[r["content"]] = {"content": r["content"], "metadata": r.get("metadata", {}), "score": 1/(i+60)}
    for i, r in enumerate(lexical_results):
        if r["content"] in merged:
            merged[r["content"]]["score"] += 1/(i+60)
        else:
            merged[r["content"]] = {"content": r["content"], "metadata": r.get("metadata", {}), "score": 1/(i+60)}
            
    candidates = list(merged.values())
    
    reranked = rerank(query, candidates, top_k=top_k)
    
    for r in reranked:
        r["source"] = "hybrid"
        
    if not reranked or reranked[0]["score"] < score_threshold:
        pageindex_results = pageindex_search(query, top_k=top_k)
        if pageindex_results:
            for r in pageindex_results:
                r["source"] = "pageindex"
            return pageindex_results
            
    return reranked

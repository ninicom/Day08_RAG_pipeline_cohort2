import os

def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    api_key = os.environ.get("PAGEINDEX_API_KEY", "")
    if not api_key:
        return []
        
    # Dummy implementation for vectorless fallback if SDK not available
    return [{
        "content": "Dummy pageindex result",
        "score": 0.5,
        "source": "pageindex",
        "metadata": {}
    }]

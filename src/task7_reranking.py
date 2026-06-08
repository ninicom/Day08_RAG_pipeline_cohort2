import os
import requests
from dotenv import load_dotenv

load_dotenv()

def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    if not candidates:
        return []
        
    api_key = os.environ.get("COHERE_API_KEY", "")
    if not api_key:
        print("Warning: COHERE_API_KEY not found in .env. Dùng tạm kết quả cũ. Vui lòng lấy key miễn phí tại dashboard.cohere.com")
        return candidates[:top_k]
        
    url = "https://api.cohere.com/v1/rerank"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    docs = [c["content"] for c in candidates]
    
    data = {
        "model": "rerank-multilingual-v3.0",
        "query": query,
        "documents": docs,
        "top_n": top_k
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            res_json = response.json()
            results = []
            for item in res_json.get("results", []):
                idx = item["index"]
                score = item["relevance_score"]
                c = candidates[idx]
                results.append({
                    "content": c["content"],
                    "score": score,
                    "metadata": c.get("metadata", {})
                })
            return results
        else:
            print(f"Reranking API Error: {response.text}")
            return candidates[:top_k]
    except Exception as e:
        print(f"Lỗi khi gọi Cohere API: {e}")
        return candidates[:top_k]

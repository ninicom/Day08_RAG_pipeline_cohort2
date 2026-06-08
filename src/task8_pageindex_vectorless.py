import os
import glob
from dotenv import load_dotenv

load_dotenv()

_pageindex_client = None

def get_client():
    global _pageindex_client
    if _pageindex_client is None:
        api_key = os.environ.get("PAGEINDEX_API_KEY", "")
        if api_key:
            try:
                from pageindex.client import PageIndexClient
                _pageindex_client = PageIndexClient(api_key=api_key)
            except ImportError:
                pass
    return _pageindex_client

def upload_missing_docs(client):
    # Use the original PDFs for PageIndex since they only support PDF
    base_dir = Path("data/landing/legal")
    doc_ids = []
    
    if not base_dir.exists():
        return doc_ids
        
    for pdf_file in base_dir.glob("*.pdf"):
        fp = str(pdf_file.resolve()) # Must be absolute or valid relative path
        try:
            print(f"Uploading {fp} to PageIndex...")
            res = client.submit_document(file_path=fp)
            if "doc_id" in res:
                doc_ids.append(res["doc_id"])
        except Exception as e:
            print(f"Error uploading {fp} to PageIndex: {e}")
    return doc_ids

def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    client = get_client()
    if not client:
        print("Warning: Không có PAGEINDEX_API_KEY, không thể dùng API thật.")
        return []
        
    try:
        doc_ids = upload_missing_docs(client)
        results = []
        for doc_id in doc_ids:
            if not doc_id: continue
            # Query document
            res = client.submit_query(doc_id=doc_id, query=query)
            
            # Format result
            # Giả định response có trường answer hoặc list of chunks
            # Extract content textually to pass back to generation
            content_str = str(res)
            if "answer" in res:
                content_str = res["answer"]
            elif "data" in res:
                content_str = str(res["data"])
                
            results.append({
                "content": f"[PageIndex Result] {content_str}",
                "score": 1.0,
                "source": "pageindex",
                "metadata": {"doc_id": doc_id}
            })
            
            if len(results) >= top_k:
                break
                
        return results
    except Exception as e:
        print(f"Error PageIndex API: {e}")
        return []

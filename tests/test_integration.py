import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    """Wait for the backend server to be available."""
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False

@pytest.fixture(scope="session", autouse=True)
def setup_server():
    if not wait_for_server():
        pytest.fail("Backend server is not running on port 8000. Please start it first.")

def test_integration_chat_endpoint():
    payload = {
        "query": "Hữu Tín",
        "useHyDE": False,
        "useReranking": False,
        "topK": 2,
        "threshold": 0.1,
        "searchMode": "Hybrid kết hợp"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    # Contract validation for Frontend normalizeSource
    for chunk in data["sources"]:
        assert "content" in chunk
        assert "score" in chunk
        assert "metadata" in chunk

def test_integration_retrieval_endpoint():
    payload = {
        "query": "Hữu Tín",
        "method": "Hybrid",
        "topK": 2,
        "threshold": 0.3
    }
    response = requests.post(f"{BASE_URL}/api/retrieval", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    # Contract validation
    for chunk in data["results"]:
        assert "content" in chunk
        assert "score" in chunk
        assert "metadata" in chunk

def test_integration_evaluation_endpoint():
    response = requests.get(f"{BASE_URL}/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data

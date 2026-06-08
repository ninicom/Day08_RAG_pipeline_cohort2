import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_endpoint():
    payload = {
        "query": "Hữu Tín ma túy",
        "useHyDE": False,
        "useReranking": False,
        "topK": 2,
        "threshold": 0.1,
        "searchMode": "Hybrid kết hợp"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)

def test_retrieval_endpoint():
    payload = {
        "query": "ma túy",
        "method": "Semantic",
        "topK": 3,
        "threshold": 0.3
    }
    response = client.post("/api/retrieval", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    if len(data["results"]) > 0:
        assert "score" in data["results"][0]

def test_evaluation_endpoint():
    response = client.get("/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "abTest" in data

def test_stats_endpoint():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "vectorStatus" in data

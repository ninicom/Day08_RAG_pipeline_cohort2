from fastapi.testclient import TestClient
from backend.main import app, session_store
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_sessions():
    session_store.clear()
    yield

@patch("backend.main.retrieve")
@patch("backend.main.generate_with_citation")
@patch("backend.main.generate_hyde_document")
def test_chat_memory_and_hyde(mock_hyde, mock_generate, mock_retrieve):
    # Setup mocks
    mock_retrieve.return_value = [{"content": "mock chunk", "score": 0.9, "metadata": {"source": "test.md"}}]
    mock_generate.return_value = {"answer": "This is a mock answer."}
    mock_hyde.return_value = "Hypothetical query about testing"

    # 1. Test basic chat without session_id (should create one)
    response = client.post("/api/chat", json={
        "query": "Hello",
        "useHyDE": False,
        "useReranking": True,
        "searchMode": "Hybrid"
    })
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["answer"] == "This is a mock answer."
    session_id = data["session_id"]
    
    # Check that memory was stored
    assert session_id in session_store
    assert len(session_store[session_id]) == 2
    assert session_store[session_id][0]["role"] == "user"
    assert session_store[session_id][1]["role"] == "assistant"
    
    # 2. Test chat with session_id
    response2 = client.post("/api/chat", json={
        "query": "Follow up question",
        "sessionId": session_id,
        "useHyDE": False,
        "searchMode": "Hybrid"
    })
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["session_id"] == session_id
    
    # Check that memory was updated
    assert len(session_store[session_id]) == 4
    
    # 3. Test HyDE
    response3 = client.post("/api/chat", json={
        "query": "Testing HyDE",
        "sessionId": session_id,
        "useHyDE": True,
        "searchMode": "Hybrid"
    })
    assert response3.status_code == 200
    assert mock_hyde.called

@patch("backend.main.retrieve")
@patch("backend.main.generate_with_citation")
def test_chat_reranking_toggle(mock_generate, mock_retrieve):
    mock_retrieve.return_value = [{"content": "mock chunk", "score": 0.9, "metadata": {"source": "test.md"}}]
    mock_generate.return_value = {"answer": "This is a mock answer."}

    # Test useReranking = False
    response = client.post("/api/chat", json={
        "query": "Hello",
        "useHyDE": False,
        "useReranking": False,
        "searchMode": "Hybrid"
    })
    assert response.status_code == 200
    # retrieve should have been called with use_reranking=False
    mock_retrieve.assert_called_with("Hello", top_k=5, score_threshold=0.3, use_reranking=False)

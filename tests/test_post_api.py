from fastapi.testclient import TestClient
from unittest.mock import patch

@patch("twitter.post_api.main.supabase")
def test_create_post(mock_supabase):
    from twitter.post_api.main import app
    client = TestClient(app)
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{"username": "bob", "content": "Hello!"}]
    
    response = client.post("/api/v1/posts?username=bob&content=Hello!")
    assert response.status_code == 200
    assert response.json()["content"] == "Hello!"
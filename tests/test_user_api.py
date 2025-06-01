from fastapi.testclient import TestClient
from unittest.mock import patch

@patch("main.supabase")
def test_create_user(mock_supabase):
    from main import app
    client = TestClient(app)
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{"username": "alice"}]
    
    response = client.post("/api/v1/users?username=alice")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

@patch("main.supabase")
def test_follow(mock_supabase):
    from main import app
    client = TestClient(app)
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{"message": "Followed successfully"}]
    
    response = client.post("/api/v1/follow?follower_username=alice&followed_username=bob")
    assert response.status_code == 200
    assert response.json()["message"] == "Followed successfully"
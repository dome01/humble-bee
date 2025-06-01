from fastapi.testclient import TestClient
from unittest.mock import patch

@patch("main.supabase")
def test_get_feed(mock_supabase):
    from main import app
    client = TestClient(app)

    # Follows lookup
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = \
        type("Res", (), {"data": [{"followed_username": "bob"}]})()

    # Posts by followed users
    mock_table = mock_supabase.table.return_value
    mock_table.select.return_value.in_.return_value.order.return_value.execute.return_value = \
        type("Res", (), {"data": [{"username": "bob", "content": "Hello from bob"}]})()

    response = client.get("/api/v1/feed?username=alice")
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["username"] == "bob"
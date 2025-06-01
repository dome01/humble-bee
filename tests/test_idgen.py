from fastapi.testclient import TestClient
from idgen_api.main import app
from unittest.mock import patch
from uuid import UUID

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello from ID-Gen!"

@patch("idgen_api.main.uuid4", return_value=UUID("00000000-0000-0000-0000-000000000000"))
@patch("idgen_api.main.supabase.table")
def test_create_id(mock_table, mock_uuid):
    mock_insert = mock_table.return_value.insert.return_value
    mock_insert.execute.return_value = {"data": [{"id": str(mock_uuid.return_value)}]}
    
    response = client.post("/ids")
    assert response.status_code == 200
    assert response.json()["id"] == "00000000-0000-0000-0000-000000000000"
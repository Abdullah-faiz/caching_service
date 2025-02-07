from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_payload():
    """Test the payload creation endpoint"""

    request_data = {
        "list_1": ["first string", "second string"],
        "list_2": ["other string", "another string"]
    }

    response = client.post("/payload", json=request_data)

    assert response.status_code == 200
    response_data = response.json()

    assert "id" in response_data
    assert response_data["output"] == "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING"

def test_get_payload():
    """Test retrieving a previously created payload"""

    request_data = {
        "list_1": ["first string", "second string"],
        "list_2": ["other string", "another string"]
    }

    post_response = client.post("/payload", json=request_data)
    payload_id = post_response.json()["id"]

    get_response = client.get(f"/payload/{payload_id}")

    assert get_response.status_code == 200
    assert get_response.json()["output"] == "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING"

def test_get_invalid_payload():
    """Test retrieving a non-existent payload"""
    
    response = client.get("/payload/invalid-id")
    assert response.status_code == 404

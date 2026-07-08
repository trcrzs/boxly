from fastapi.testclient import TestClient

from app.main import app
import uuid

client = TestClient(app)

def test_register_user():

	unique_email = f"testuser_{uuid.uuid4()}@example.com"

	response = client.post("/users/register",
		json = {
				"name": "Test User",
				"email": unique_email,
				"password": "Test123!"
			}
		)

	assert response.status_code == 200
	assert response.json()["name"] == "Test User"
	assert response.json()["email"] == unique_email
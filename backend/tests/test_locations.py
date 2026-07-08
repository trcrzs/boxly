from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_location():
	login_response = client.post("/auth/login",
		data = {
			"username": "testuser@example.com",
			"password": "Test123!"
			}
		)

	assert login_response.status_code == 200

	token = login_response.json()["access_token"]

	response = client.post("/locations/",
		json = {
			"name": "Example Location",
			"description": "Example description."
			},
			headers = {
				"Authorization": f"Bearer {token}"
			}
		)

	assert response.status_code == 200
	assert response.json()["name"] == "Example Location"
	assert response.json()["description"] == "Example description."

def test_get_locations():
	login_response = client.post("/auth/login",
		data = {
			"username": "testuser@example.com",
			"password": "Test123!"
			}
		)

	assert login_response.status_code == 200

	token = login_response.json()["access_token"]

	response = client.get("/locations/",
			headers = {
				"Authorization": f"Bearer {token}"
			}
		)

	assert response.status_code == 200
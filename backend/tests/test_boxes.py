from fastapi.testclient import TestClient

from app.main import app
import uuid

client = TestClient(app)


def test_create_box():
	login_response = client.post("/auth/login",
		data = {
			"username": "testuser@example.com",
			"password": "Test123!"
			}
		)

	assert login_response.status_code == 200

	token = login_response.json()["access_token"]

	location_response = client.post("/locations/",
		json = {
			"name": f"Box Test Location {uuid.uuid4()}",
			"description": "Location for box test."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	assert location_response.status_code == 200

	location_id = location_response.json()["id"]

	storage_area_response = client.post("/storage_areas/",
		json = {
			"location_id": location_id,
			"name": "Top Shelf",
			"description": "Shelf for box test."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	assert storage_area_response.status_code == 200

	storage_area_id = storage_area_response.json()["id"]

	response = client.post("/containers/",
		json = {
			"storage_area_id": storage_area_id,
			"name": "Tool Box",
			"description": "Main tool box",
			"color": "Red"
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	assert response.status_code == 200
	assert response.json()["storage_area_id"] == storage_area_id
	assert response.json()["name"] == "Tool Box"
	assert response.json()["description"] == "Main tool box"
	assert response.json()["color"] == "Red"
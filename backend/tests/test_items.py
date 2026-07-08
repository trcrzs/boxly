from fastapi.testclient import TestClient

from app.main import app
import uuid

client = TestClient(app)


def test_create_item():
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
			"name": f"Item Test Location {uuid.uuid4()}",
			"description": "Location for item test."
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
			"name": "Item Test Storage Area",
			"description": "Storage area for item test."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	assert storage_area_response.status_code == 200

	storage_area_id = storage_area_response.json()["id"]

	box_response = client.post("/containers/",
		json = {
			"storage_area_id": storage_area_id,
			"name": "Item Test Box",
			"description": "Box for item test.",
			"color": "Blue"
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	assert box_response.status_code == 200

	box_id = box_response.json()["id"]

	response = client.post("/items/",
		json = {
			"box_id": box_id,
			"name": "Hammer",
			"description": "Small claw hammer"
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	assert response.status_code == 200
	assert response.json()["box_id"] == box_id
	assert response.json()["name"] == "Hammer"
	assert response.json()["description"] == "Small claw hammer"


def test_search_items():
	login_response = client.post("/auth/login",
		data = {
			"username": "testuser@example.com",
			"password": "Test123!"
			}
		)

	assert login_response.status_code == 200

	token = login_response.json()["access_token"]

	response = client.get("/items/search?name=Hammer",
		headers = {
			"Authorization": f"Bearer {token}"
			}
		)

	assert response.status_code == 200

	items = response.json()

	assert isinstance(items, list)
	assert len(items) > 0
	assert items[0]["name"] == "Hammer"
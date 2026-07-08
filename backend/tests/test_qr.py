from fastapi.testclient import TestClient

from app.main import app
import uuid

client = TestClient(app)


def test_qr_endpoint_returns_url():
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
			"name": f"QR Test Location {uuid.uuid4()}",
			"description": "Location for QR test."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	location_id = location_response.json()["id"]

	storage_area_response = client.post("/storage_areas/",
		json = {
			"location_id": location_id,
			"name": "QR Test Storage Area",
			"description": "Storage area for QR test."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	storage_area_id = storage_area_response.json()["id"]

	box_response = client.post("/containers/",
		json = {
			"storage_area_id": storage_area_id,
			"name": "QR Test Box",
			"description": "Box for QR test.",
			"color": "Black"
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	box_id = box_response.json()["id"]

	response = client.get(f"/containers/{box_id}/qr",
		headers = {
			"Authorization": f"Bearer {token}"
			}
		)

	assert response.status_code == 200
	assert "qr_code_url" in response.json()


def test_public_box_endpoint():
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
			"name": f"Public QR Test {uuid.uuid4()}",
			"description": "Location for public QR test."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	location_id = location_response.json()["id"]

	storage_area_response = client.post("/storage_areas/",
		json = {
			"location_id": location_id,
			"name": "Public Storage Area",
			"description": "Storage area."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	storage_area_id = storage_area_response.json()["id"]

	box_response = client.post("/containers/",
		json = {
			"storage_area_id": storage_area_id,
			"name": "Public Box",
			"description": "Box for public endpoint.",
			"color": "Green"
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	box_id = box_response.json()["id"]

	item_response = client.post("/items/",
		json = {
			"box_id": box_id,
			"name": "Screwdriver",
			"description": "Flathead screwdriver."
			},
			headers = {
				"Authorization": f"Bearer {token}"
				}
		)

	assert item_response.status_code == 200

	response = client.get(f"/containers/public/{box_id}")

	assert response.status_code == 200
	assert "box" in response.json()
	assert "items" in response.json()
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_storage_area():
    login_response = client.post("/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "Test123!"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    location_response = client.post(
        "/locations/",
        json={
            "name": "Storage Area Test Location",
            "description": "Location for testing storage areas."
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert location_response.status_code == 200

    location_id = location_response.json()["id"]

    response = client.post(
        "/storage_areas/",
        json={
            "location_id": location_id,
            "name": "Test storage area",
            "description": "Test description"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["location_id"] == location_id
    assert response.json()["name"] == "Test storage area"
    assert response.json()["description"] == "Test description"

def test_get_storage_areas():
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "Test123!"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/storage_areas/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    storage_areas = response.json()

    assert isinstance(storage_areas, list)
    assert len(storage_areas) > 0
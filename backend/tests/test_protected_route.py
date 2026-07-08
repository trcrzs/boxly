from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_protected_route_requires_token():
	response = client.get("/locations/")

	assert response.status_code == 401
	assert response.json()["detail"] == "Not authenticated"
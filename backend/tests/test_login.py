from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_login_user():
	response = client.post("/auth/login", data = {
		"username": "testuser@example.com",
		"password": "Test123!"
		}
	)
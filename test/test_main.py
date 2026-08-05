from fastapi.testclient import TestClient
from app.main import app

baby = TestClient(app)

def test_da_main():
    response = baby.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to cloud sentinel!"}

def test_da_health():
    response = baby.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "Version": "0.1.0"}

    


from fastapi.testclient import TestClient
from app.main import app

boba = TestClient(app)

def test_da_create():
    response = boba.get("/metrics")
    assert response.status_code == 200
    assert response.json() == {"uptime_seconds": round(uptime_seconds, 2),
            "request_count": REQUEST_COUNT}
    

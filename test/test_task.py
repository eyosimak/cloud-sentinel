from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
        autoflush=False, autocommit=False, bind=engine
)
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_function():
    Base.metadata.create_all(bind=engine)
def downup_function():
    Base.metadata.drop_all(bind=engine)
def test_create_task():
    response = client.post(
            "/tasks/",
            json={
                "title": "Test Task",
                "status": "pending",
                "priority": "high",
            },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert "id" in data

def test_read_task():
    client.post("/tasks/", json={"title": "Task One"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[-1]["title"] == "Task One"

def test_read_single_task():
    create_response = client.post("/tasks", json={"title": "Specific Task"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"

def test_update_task():
    create_response = client.post(
            "/tasks/", json={"title": "old title", "status": "pending"}
    )
    task_id = create_response.json()["id"]
    response = client.put(
            f"/tasks/{task_id}", json={"title": "new title", "status": "completed"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "new title"
    assert data["status"] == "completed"

def test_delete_task():
    create_response = client.post(
            "/tasks/", json={"title": "task to delete"}
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


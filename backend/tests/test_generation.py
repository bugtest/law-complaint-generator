import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    return login_response.json()["access_token"]

def test_generate_without_elements(client, auth_token):
    case_response = client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    case_id = case_response.json()["id"]

    response = client.post(f"/api/cases/{case_id}/generate", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 400

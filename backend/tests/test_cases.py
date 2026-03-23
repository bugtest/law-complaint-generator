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

def test_create_case(client, auth_token):
    response = client.post("/api/cases", json={
        "case_name": "张三诉李四借款纠纷案"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["case_name"] == "张三诉李四借款纠纷案"
    assert "id" in data

def test_get_cases(client, auth_token):
    client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.get("/api/cases", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_case(client, auth_token):
    create_response = client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    case_id = create_response.json()["id"]

    response = client.get(f"/api/cases/{case_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json()["id"] == case_id

def test_delete_case(client, auth_token):
    create_response = client.post("/api/cases", json={
        "case_name": "Test Case"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    case_id = create_response.json()["id"]

    response = client.delete(f"/api/cases/{case_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 204

    get_response = client.get(f"/api/cases/{case_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert get_response.status_code == 404

import pytest
from app.database import engine, Base
from app.main import app

@pytest.fixture(scope="function")
def test_db():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Create test client"""
    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    """Register and login to get auth token"""
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

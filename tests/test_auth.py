import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# -------------------------------
# Setup: Test DB and session
# -------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# -------------------------------
# Fixture: Reset DB per test
# -------------------------------
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# -------------------------------
# Test: Registration
# -------------------------------
def test_register_user_success():
    response = client.post("/register", json={
        "email": "user@example.com",
        "password": "StrongPass1!"
    })
    assert response.status_code == 200
    assert "registered successfully" in response.json()["message"]

def test_register_user_duplicate():
    client.post("/register", json={
        "email": "dupe@example.com",
        "password": "StrongPass1!"
    })
    response = client.post("/register", json={
        "email": "dupe@example.com",
        "password": "StrongPass1!"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_register_user_weak_password():
    response = client.post("/register", json={
        "email": "user2@example.com",
        "password": "weak"
    })
    assert response.status_code == 422  # Pydantic validation error

def test_register_invalid_email():
    response = client.post("/register", json={
        "email": "notanemail",
        "password": "StrongPass1!"
    })
    assert response.status_code == 422

# -------------------------------
# Test: Login
# -------------------------------
def test_login_success():
    client.post("/register", json={
        "email": "login@example.com",
        "password": "StrongPass1!"
    })
    response = client.post("/login", json={
        "email": "login@example.com",
        "password": "StrongPass1!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    client.post("/register", json={
        "email": "wrongpass@example.com",
        "password": "RightPass1!"
    })
    response = client.post("/login", json={
        "email": "wrongpass@example.com",
        "password": "WrongPass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"

def test_login_user_not_found():
    response = client.post("/login", json={
        "email": "ghost@example.com",
        "password": "DoesntMatter1!"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

# -------------------------------
# Test: Protected route
# -------------------------------
def test_protected_route_access():
    # Register and login to get token
    client.post("/register", json={
        "email": "secure@example.com",
        "password": "ValidPass1!"
    })
    login = client.post("/login", json={
        "email": "secure@example.com",
        "password": "ValidPass1!"
    })
    token = login.json()["access_token"]

    # Access protected route with token
    response = client.get("/protected", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert "secure@example.com" in response.json()["message"]

def test_protected_route_no_token():
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_protected_route_invalid_token():
    response = client.get("/protected", headers={
        "Authorization": "Bearer fake.invalid.token"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"

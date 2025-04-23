# -----------------------------
# Test client and app imports
# -----------------------------
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# -----------------------------
# Setup: In-memory SQLite test DB
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"  # or use sqlite:///:memory: for pure in-memory
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database schema before tests run
Base.metadata.create_all(bind=engine)

# Override the get_db dependency
def override_get_db():
    """
    Overrides the get_db dependency to use the in-memory SQLite database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# -----------------------------
# Fixture: Reset database before each test
# -----------------------------
@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """
    Resets the database before each test.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
# -----------------------------
# Test: Successful user registration
# -----------------------------
def test_register_user_success():
    """
    Tests if a new user can be registered successfully.
    """
    response = client.post("/register", json={
        "username": "testuser1",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User testuser1 registered successfully"

# -----------------------------
# Test: Duplicate registration
# -----------------------------
def test_register_user_duplicate():
    """
    Tests if registering the same user twice results in an error.
    """
    client.post("/register", json={
        "username": "dupeuser",
        "password": "pass123"
    })
    response = client.post("/register", json={
        "username": "dupeuser",
        "password": "pass123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

# -----------------------------
# Test: Registration with empty fields
# -----------------------------
def test_register_user_empty_fields():
    """
    Tests if registration fails when username or password is empty.
    """
    response = client.post("/register", json={
        "username": "",
        "password": "testpass123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username and password are required"

    response = client.post("/register", json={
        "username": "testuser",
        "password": ""
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username and password are required"

# -----------------------------
# Test: Successful login
# -----------------------------
def test_login_success():
    """
    Tests if a user can log in and receive a valid JWT token.
    """
    client.post("/register", json={
        "username": "loginuser",
        "password": "securepass"
    })
    response = client.post("/login", json={
        "username": "loginuser",
        "password": "securepass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# -----------------------------
# Test: Login with wrong password
# -----------------------------
def test_login_wrong_password():
    """
    Tests login failure when password is incorrect.
    """
    client.post("/register", json={
        "username": "wrongpassuser",
        "password": "rightpass"
    })
    response = client.post("/login", json={
        "username": "wrongpassuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"

# -----------------------------
# Test: Login with nonexistent user
# -----------------------------
def test_login_user_not_found():
    """
    Tests login failure when username is not found.
    """
    response = client.post("/login", json={
        "username": "ghostuser",
        "password": "doesntmatter"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

# -----------------------------
# Test: Access protected route without token
# -----------------------------
def test_protected_route_without_token():
    """
    Tests if protected route rejects unauthenticated requests.
    """
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# -----------------------------
# Test: Access protected route with valid token
# -----------------------------
def test_protected_route_with_valid_token():
    """
    Tests if protected route can be accessed with a valid token.
    """
    client.post("/register", json={
        "username": "authuser",
        "password": "validpass"
    })
    login_response = client.post("/login", json={
        "username": "authuser",
        "password": "validpass"
    })
    token = login_response.json()["access_token"]
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Hello, authuser" in response.json()["message"]

# -----------------------------
# Test: Access protected route with invalid token
# -----------------------------
def test_protected_route_invalid_token():
    """
    Tests if protected route rejects requests with an invalid token format.
    """
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"
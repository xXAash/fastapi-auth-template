from fastapi.testclient import TestClient
from microservices.auth.main import app

client = TestClient(app)

def test_register_user_success():
    response = client.post("/register", json={
        "username": "testuser1",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User testuser1 registered successfully"

def test_register_user_duplicate():
    # Register user the first time
    client.post("/register", json={
        "username": "dupeuser",
        "password": "pass123"
    })

    # Try registering same user again
    response = client.post("/register", json={
        "username": "dupeuser",
        "password": "pass123"
    })

    assert response.status_code == 200  # still 200, but has an error message
    assert response.json()["error"] == "User already exists"

def test_login_success():
    # Register a fresh user
    client.post("/register", json={
        "username": "loginuser",
        "password": "securepass"
    })

    # Try logging in
    response = client.post("/login", json={
        "username": "loginuser",
        "password": "securepass"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Logged in as loginuser"


def test_login_wrong_password():
    # Register a fresh user
    client.post("/register", json={
        "username": "wrongpassuser",
        "password": "rightpass"
    })

    # Try logging in with wrong password
    response = client.post("/login", json={
        "username": "wrongpassuser",
        "password": "wrongpass"
    })

    assert response.status_code == 200
    assert response.json()["error"] == "Incorrect password"

def test_login_user_not_found():
    response = client.post("/login", json={
        "username": "ghostuser",
        "password": "doesntmatter"
    })

    assert response.status_code == 200
    assert response.json()["error"] == "User not found"

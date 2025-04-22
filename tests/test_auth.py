# -----------------------------
# Test client and app imports
# -----------------------------
from fastapi.testclient import TestClient
from microservices.auth.main import app

# -----------------------------
# Setup test client
# -----------------------------
client = TestClient(app)

# -----------------------------
# Test: Successful user registration
# -----------------------------
def test_register_user_success():
    """
    Should successfully register a new user.
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
    Should return error if username is already taken.
    """
    client.post("/register", json={
        "username": "dupeuser",
        "password": "pass123"
    })

    response = client.post("/register", json={
        "username": "dupeuser",
        "password": "pass123"
    })

    assert response.status_code == 200
    assert response.json()["error"] == "User already exists"

# -----------------------------
# Test: Successful login
# -----------------------------
def test_login_success():
    """
    Should return a JWT token when login credentials are valid.
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
    Should return error when password is incorrect.
    """
    client.post("/register", json={
        "username": "wrongpassuser",
        "password": "rightpass"
    })

    response = client.post("/login", json={
        "username": "wrongpassuser",
        "password": "wrongpass"
    })

    assert response.status_code == 200
    assert response.json()["error"] == "Incorrect password"

# -----------------------------
# Test: Login with nonexistent user
# -----------------------------
def test_login_user_not_found():
    """
    Should return error when username is not found.
    """
    response = client.post("/login", json={
        "username": "ghostuser",
        "password": "doesntmatter"
    })

    assert response.status_code == 200
    assert response.json()["error"] == "User not found"

# -----------------------------
# Test: Access protected route without token
# -----------------------------
def test_protected_route_without_token():
    """
    Should return 401 Unauthorized when no token is provided.
    """
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# -----------------------------
# Test: Access protected route with valid token
# -----------------------------
def test_protected_route_with_valid_token():
    """
    Should return success when a valid JWT token is provided.
    """
    # Register and login to get a token
    client.post("/register", json={
        "username": "authuser",
        "password": "validpass"
    })
    login_response = client.post("/login", json={
        "username": "authuser",
        "password": "validpass"
    })
    token = login_response.json()["access_token"]

    # Access protected route with Bearer token
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "Hello, authuser" in response.json()["message"]
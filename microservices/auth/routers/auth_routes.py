# -------------------------
# External dependencies
# -------------------------
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext

# -------------------------
# Internal utility imports
# -------------------------
from microservices.auth.utils.jwt_utils import create_access_token, verify_access_token

# -------------------------
# Temporary in-memory "database"
# (replace with actual DB in production)
# -------------------------
fake_users_db = {}

# -------------------------
# Password hashing setup using bcrypt
# -------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    Returns the hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against the stored hash.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------
# FastAPI router instance
# -------------------------
router = APIRouter()

# -------------------------
# OAuth2 setup for protected routes
# -------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------
# Request models
# -------------------------

class RegisterRequest(BaseModel):
    """
    Request body model for user registration.
    """
    username: str
    password: str

class LoginRequest(BaseModel):
    """
    Request body model for user login.
    """
    username: str
    password: str

# -------------------------
# /register route
# -------------------------

@router.post("/register")
async def register(payload: RegisterRequest):
    """
    Register a new user.
    - Checks if user already exists
    - Hashes password and stores user
    - Returns success or error message
    """
    if payload.username in fake_users_db:
        return {"error": "User already exists"}

    hashed_pw = hash_password(payload.password)

    fake_users_db[payload.username] = {
        "username": payload.username,
        "password": hashed_pw
    }

    return {"message": f"User {payload.username} registered successfully"}

# -------------------------
# /login route
# -------------------------

@router.post("/login")
async def login(payload: LoginRequest):
    """
    Authenticate a user and return a JWT access token.
    - Validates username/password
    - Returns error on failure or token on success
    """
    user = fake_users_db.get(payload.username)
    if not user:
        return {"error": "User not found"}

    if not verify_password(payload.password, user["password"]):
        return {"error": "Incorrect password"}

    access_token = create_access_token(data={"sub": payload.username})
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------
# /protected route (JWT required)
# -------------------------

@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    """
    A test-protected route that requires a valid JWT token.
    Returns a greeting with the user's username.
    """
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    return {"message": f"Hello, {username}. You have access!"}
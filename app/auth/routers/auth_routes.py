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
from app.auth.utils.jwt_utils import create_access_token, verify_access_token
from app.auth.models import User
from app.database import get_db

# -------------------------
# Database Connection and ORM imports
# -------------------------
from sqlalchemy.orm import Session

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
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Checks if user already exists
    - Hashes password and stores user
    - Returns success or error message
    """
    # Validate input
    if not payload.username.strip() or not payload.password.strip():
        raise HTTPException(status_code=400, detail="Username and password are required")

    # Check if the user already exists in the database
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password and create a new user
    hashed_pw = hash_password(payload.password)
    new_user = User(username=payload.username, password=hashed_pw)
    db.add(new_user)
    db.commit()

    return {"message": f"User {payload.username} registered successfully"}

# -------------------------
# /login route
# -------------------------

@router.post("/login")
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.
    - Validates username/password
    - Returns error on failure or token on success
    """
    # Fetch the user from the database
    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the password
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Create a JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------
# /protected route (JWT required)
# -------------------------

@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    A test-protected route that requires a valid JWT token.
    Returns a greeting with the user's username.
    """
    # Verify the JWT token
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch the user from the database (optional)
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"Hello, {user.username}. You have access!"}
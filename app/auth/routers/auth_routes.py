# -------------------------
# External dependencies
# -------------------------
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, field_validator
from passlib.context import CryptContext
import re

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
    """
    return pwd_context.hash(password) # Return the hashed password.

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against the stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password) # Return True if the password matches, False otherwise.

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
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def strong_password(cls, value):
        allowed_specials = "!@#$%^&*()_+-=.?/"
        special_char_pattern = f"[{re.escape(allowed_specials)}]"

        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(special_char_pattern, value):
            raise ValueError(f"Password must contain at least one special character from: {allowed_specials}")
        if re.search(rf"[^\w\d{re.escape(allowed_specials)}]", value):
            raise ValueError("Password contains invalid characters")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# -------------------------
# /register route
# -------------------------
@router.post("/register")
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(payload.password)
    new_user = User(email=payload.email, password=hashed_pw)
    db.add(new_user)
    db.commit()

    return {"message": f"User {payload.email} registered successfully"}

# -------------------------
# /login route
# -------------------------
@router.post("/login")
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------
# /protected route (JWT required)
# -------------------------
@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"Hello, {user.email}. You have access!"}
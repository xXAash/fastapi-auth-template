from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext

# Temporary "database"
fake_users_db = {}

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(payload: LoginRequest):
    user = fake_users_db.get(payload.username)
    if not user:
        return {"error": "User not found"}

    if not verify_password(payload.password, user["password"]):
        return {"error": "Incorrect password"}

    return {"message": f"Logged in as {payload.username}"}

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(payload: RegisterRequest):
    if payload.username in fake_users_db:
        return {"error": "User already exists"}

    hashed_pw = hash_password(payload.password)
    fake_users_db[payload.username] = {
        "username": payload.username,
        "password": hashed_pw
    }

    return {"message": f"User {payload.username} registered successfully"}

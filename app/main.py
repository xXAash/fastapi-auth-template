# -----------------------------
# FastAPI App Entry Point
# -----------------------------

from fastapi import FastAPI  # FastAPI framework core
from app.auth.routers.auth_routes import router  # Importing the auth router

# -----------------------------
# Initialize FastAPI App
# -----------------------------
app = FastAPI()

# -----------------------------
# Register Routers
# -----------------------------
# The auth router handles routes like /login, /register, /protected
# As your project grows, more routers (e.g., savings, debt) can be added here
app.include_router(router)

# -----------------------------
# Basic Root Route for Welcome Message
# -----------------------------
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Authentication Backend!"}
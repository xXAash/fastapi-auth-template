# ----------------------------
# JWT Token Utility Functions
# ----------------------------

import os
from dotenv import load_dotenv  # For loading environment variables from .env file
from jose import JWTError, jwt  # JWTError for validation, jwt to encode/decode tokens
from datetime import datetime, timedelta, timezone  # Used for setting expiration

load_dotenv()  # Load environment variables from .env file

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set. Please define it in your .env file.")

# ----------------------------
# JWT Configuration
# ----------------------------

# Load secret key from environment
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))

# ----------------------------
# Create Access Token
# ----------------------------

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a JWT token containing provided user data.
    Args:
        data (dict): The data to encode in the token (e.g., {"sub": "username"})
        expires_delta (timedelta, optional): Custom expiration. Defaults to 60 mins.
    Returns:
        str: Encoded JWT token as a string
    """
    to_encode = data.copy()

    # Set token expiration (timezone-aware UTC)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Encode the token using the secret and algorithm
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ----------------------------
# Verify Access Token
# ----------------------------

def verify_access_token(token: str):
    """
    Decodes and verifies a JWT token.
    Args:
        token (str): The token string from the Authorization header
    Returns:
        dict: Decoded payload if token is valid
        None: If the token is invalid or expired
    """
    try:
        # Decode and validate token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # e.g., {"sub": "username", "exp": "..."}
    except JWTError:
        return None  # Invalid signature, expired token, malformed token
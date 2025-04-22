# ----------------------------
# JWT Token Utility Functions
# ----------------------------

import os
from dotenv import load_dotenv  # For loading environment variables from .env file
from jose import JWTError, jwt  # JWTError for validation, jwt to encode/decode tokens
from datetime import datetime, timedelta, timezone  # Used for setting expiration

load_dotenv()  # Load environment variables from .env file

# ----------------------------
# JWT Configuration
# ----------------------------

# Load secret key from environment
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"  # JWT algorithm used for encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Default token expiry (60 minutes)

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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # e.g., {"sub": "username", "exp": "..."}
    except JWTError:
        return None  # Invalid signature, expired token, malformed token
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Secret Key (Change this in production!)
SECRET_KEY = "a94d5f0e4e1b2f85e2c5d7a97d26fae3a23456789abcdef1234567890abcdef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes the given password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        print(f"🔑 Created JWT Token: {encoded_jwt}")  # Debugging line

        return encoded_jwt

    except Exception as e:
        print(f"🚨 Error creating token: {e}")  # Debugging line
        raise HTTPException(status_code=500, detail="Token generation failed")


def decode_access_token(token: str):
    """
    Decodes a JWT token and extracts the user_id.

    Args:
        token (str): JWT token.

    Returns:
        int: Decoded user_id or None if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)  # Convert back to integer
    except JWTError:
        return None

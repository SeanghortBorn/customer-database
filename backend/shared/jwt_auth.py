"""JWT Authentication utilities for handling user authentication without Supabase"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from uuid import UUID
import os

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY or SECRET_KEY == "your-secret-key-change-in-production":
    print("⚠️  WARNING: JWT_SECRET_KEY not set or using default value!")
    print("⚠️  Please set JWT_SECRET_KEY environment variable in production")
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production-INSECURE")
    
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Convert strings to bytes
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception as e:
        print(f"❌ Password verification error: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt directly (bypassing passlib to avoid the 72-byte bug)"""
    try:
        # Convert to bytes
        password_bytes = password.encode('utf-8')
        
        # Truncate to 72 bytes if needed (bcrypt hard limit)
        if len(password_bytes) > 72:
            print(f"⚠️  Password is {len(password_bytes)} bytes, truncating to 72")
            password_bytes = password_bytes[:72]
        
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode('utf-8')
    except Exception as e:
        print(f"❌ Error hashing password: {str(e)}")
        print(f"   Password length: {len(password)} chars, {len(password.encode('utf-8'))} bytes")
        raise Exception(f"Failed to hash password: {str(e)}")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

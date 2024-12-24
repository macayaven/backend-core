# backend_core/core/security.py
"""Security utilities."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from backend_core.core.settings import settings

# Configure CryptContext with bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    verified: bool = pwd_context.verify(plain_password, hashed_password)
    return verified


def get_password_hash(password: str) -> str:
    """Hash a password."""
    hashed_password: str = pwd_context.hash(password)
    return hashed_password


def create_access_token(email: EmailStr, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(email)}
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

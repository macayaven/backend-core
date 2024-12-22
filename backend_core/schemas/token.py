# backend_core/schemas/token.py
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Token payload schema."""

    sub: str  # subject (user email)
    exp: int  # expiration time


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
